# Relative path: src/ai/gemini_client.py
import logging
import os
import json # For parsing JSON response from AI
from typing import Optional

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from src.ai.ai_client_interface import AIClientInterface
from src.ai.evaluation_result import EvaluationResult # Import the new result class

# Set up logging for this module
logger = logging.getLogger(__name__)

class GeminiClient(AIClientInterface):
    """
    An AI client implementation for Google Gemini API.
    Handles communication with the Gemini model for evaluating user answers.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash") -> None:
        """
        Initializes the GeminiClient.

        Args:
            api_key (str): Your Google Gemini API key.
            model_name (str): The name of the Gemini model to use (e.g., "gemini-1.5-flash").
        """
        if not api_key:
            logger.error("Gemini API key is missing. AI evaluation will not work.")
            raise ValueError("Gemini API key must be provided.")

        self._model_name: str = model_name
        self._api_key: str = api_key
        try:
            genai.configure(api_key=self._api_key)
            self._model = genai.GenerativeModel(self._model_name)
            logger.info(f"GeminiClient initialized with model: {self._model_name}")
        except Exception as e:
            logger.critical(f"Failed to configure Google Gemini API or load model: {e}")
            raise RuntimeError(f"Could not initialize Gemini model: {e}") from e

    def evaluate_answer(
        self,
        question_front: str,
        correct_back: str,
        user_answer: str,
        evaluation_hint: Optional[str] = None
    ) -> EvaluationResult:
        """
        Evaluates a user's answer against the correct answer using the Gemini AI model.

        The AI assesses the user's answer and is instructed to return a JSON object
        containing the correctness and an explanation for incorrect answers.

        Args:
            question_front (str): The question text from the flashcard.
            correct_back (str): The correct answer text from the flashcard.
            user_answer (str): The user's provided answer.
            evaluation_hint (Optional[str], optional): An optional hint to guide the AI's
                                                       evaluation process. Defaults to None.

        Returns:
            EvaluationResult: An object containing a boolean for correctness and an
                              optional string explanation.
        """
        if not self._model:
            logger.error("Gemini model is not initialized. Cannot evaluate answer.")
            return EvaluationResult(is_correct=False, explanation="AI model not initialized.")

        prompt_lines = [
            "You are an AI assistant evaluating answers for a flashcard quiz.",
            "Your task is to determine if the user's answer is correct and provide a brief explanation if it's incorrect.",
            "Respond ONLY with a single, valid JSON object containing two keys:",
            "1. \"is_correct\": A boolean value (true if the user's answer is substantially correct, false otherwise).",
            "2. \"explanation\": A string. If \"is_correct\" is false, this string should contain a brief, user-friendly explanation of why the user's answer is incorrect (e.g., what was wrong, what was missing). If \"is_correct\" is true, this string should be null or an empty string.\n",
            f"Flashcard Question: \"{question_front}\"",
            f"Correct Answer (Back of Flashcard): \"{correct_back}\"",
            f"User's Answer: \"{user_answer}\""
            f"If not specified in the evaluation hint: letter case is not important."
            f"If not specified in the evaluation hint: small typos are acceptable."
            f"If not specified in the evaluation hint: order of key-words is not important."
            f"If not specified in the evaluation hint and the correct answer is some sort of a list: user must provide all items in the list, without any additional items."
            f"If not specified in the evaluation hint and correct answer consist of some kind of senteces or phrases: user's response don't have to be EXACTLY the same, but must be valid paraphrase of the correct answer."
        ]
        if evaluation_hint:
            prompt_lines.append(f"Evaluation Hint: \"{evaluation_hint}\"")
        
        prompt_lines.append("\nExample of your JSON response if the user was incorrect:")
        prompt_lines.append("{\n  \"is_correct\": false,\n  \"explanation\": \"Your answer missed mentioning 'X' and incorrectly stated 'Y'.\"\n}")
        prompt_lines.append("\nExample of your JSON response if the user was correct:")
        prompt_lines.append("{\n  \"is_correct\": true,\n  \"explanation\": null\n}")
        prompt_lines.append("\nNow, evaluate the provided user's answer and provide your JSON response:")

        prompt = "\n".join(prompt_lines)
        logger.debug(f"Sending prompt to Gemini: {prompt}")

        try:
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            response = self._model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0, # Aim for deterministic and structured output
                    # max_output_tokens might need to be adjusted if explanations are long
                    # For now, let's assume explanations are reasonably short.
                )
            )
            
            if not response.parts or not response.parts[0].text:
                logger.warning(f"Gemini returned empty response for question: '{question_front}'. Assuming incorrect.")
                return EvaluationResult(is_correct=False, explanation="AI returned an empty response.")

            ai_response_text = response.parts[0].text.strip()
            logger.debug(f"Gemini raw response text: '{ai_response_text}'")

            # Attempt to parse the JSON response
            try:
                # The response might be wrapped in markdown ```json ... ```
                if ai_response_text.startswith("```json"):
                    ai_response_text = ai_response_text[len("```json"):].strip()
                if ai_response_text.endswith("```"):
                    ai_response_text = ai_response_text[:-len("```")].strip()
                
                parsed_json = json.loads(ai_response_text)
                is_correct = parsed_json.get("is_correct")
                explanation = parsed_json.get("explanation")

                if isinstance(is_correct, bool):
                    # Ensure explanation is a string or None
                    if explanation is not None and not isinstance(explanation, str):
                        logger.warning(f"AI returned non-string explanation: {explanation}. Setting to None.")
                        explanation = str(explanation) # Or None, depending on desired strictness
                    
                    # If correct, explanation should ideally be null/empty, but we prioritize is_correct
                    if is_correct and explanation == "": 
                        explanation = None # Normalize empty string to None for consistency

                    return EvaluationResult(is_correct=is_correct, explanation=explanation)
                else:
                    logger.error(f"Gemini JSON response missing or invalid 'is_correct' boolean for question: '{question_front}'. Response: {ai_response_text}")
                    return EvaluationResult(is_correct=False, explanation="AI response format error (is_correct field).")

            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from Gemini response: {e}. Response: {ai_response_text}")
                # Fallback: try a simple YES/NO check on the raw text if it's very short
                if ai_response_text.upper() == "YES":
                    return EvaluationResult(is_correct=True)
                elif ai_response_text.upper() == "NO":
                    return EvaluationResult(is_correct=False, explanation="AI response was not valid JSON, but indicated 'NO'.")
                return EvaluationResult(is_correct=False, explanation="AI response was not valid JSON.")
            except AttributeError as e: # If parsed_json is not a dict
                logger.error(f"Gemini JSON response was not a dictionary: {e}. Response: {ai_response_text}")
                return EvaluationResult(is_correct=False, explanation="AI response format error (not a dictionary).")


        except genai.types.BlockedPromptException as e:
            logger.error(f"Gemini API blocked the prompt due to safety reasons: {e}")
            return EvaluationResult(is_correct=False, explanation="Prompt blocked by AI safety filters.")
        except Exception as e:
            logger.error(f"An error occurred during Gemini API call: {e}", exc_info=True)
            return EvaluationResult(is_correct=False, explanation=f"AI API call error: {e}")

# Example usage (requires an actual API key to run successfully)
if __name__ == '__main__':
    from src.core.logger_setup import setup_logging
    try:
        setup_logging({'log_level': 'DEBUG', 'log_to_console': True, 'log_to_file': False})
    except TypeError:
        setup_logging('DEBUG')

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        gemini_api_key = "YOUR_GEMINI_API_KEY" 

    if gemini_api_key == "YOUR_GEMINI_API_KEY":
        logger.warning("Please set the GEMINI_API_KEY environment variable or replace 'YOUR_GEMINI_API_KEY' in the test.")
        print("Skipping GeminiClient direct test due to missing API key.")
    else:
        try:
            gemini_client = GeminiClient(api_key=gemini_api_key, model_name="gemini-1.5-flash")

            print("\n--- Testing GeminiClient with JSON output ---")
            
            q1 = "What is the capital of France?"
            a1_correct_ans = "Paris"
            
            # Test 1: Correct user answer
            user_ans_correct = "Paris"
            eval_res1 = gemini_client.evaluate_answer(q1, a1_correct_ans, user_ans_correct)
            print(f"Q: {q1}, Correct: {a1_correct_ans}, User: '{user_ans_correct}' -> AI Correct: {eval_res1.is_correct}, Explanation: {eval_res1.explanation}")

            # Test 2: Incorrect user answer
            user_ans_incorrect = "London"
            eval_res2 = gemini_client.evaluate_answer(q1, a1_correct_ans, user_ans_incorrect)
            print(f"Q: {q1}, Correct: {a1_correct_ans}, User: '{user_ans_incorrect}' -> AI Correct: {eval_res2.is_correct}, Explanation: {eval_res2.explanation}")

            # Test 3: Partially correct user answer
            user_ans_partial = "The capital is PParis but I'm not sure." # Deliberate typo
            hint3 = "Focus on the city name. Ignore surrounding text unless it contradicts."
            eval_res3 = gemini_client.evaluate_answer(q1, a1_correct_ans, user_ans_partial, evaluation_hint=hint3)
            print(f"Q: {q1}, Correct: {a1_correct_ans}, User: '{user_ans_partial}' (Hint: {hint3}) -> AI Correct: {eval_res3.is_correct}, Explanation: {eval_res3.explanation}")

            # Test 4: Example from user prompt
            q4 = "Podaj owoce które lubisz"
            a4_correct = "jabłko, pomarańcza, banan"
            user_ans_q4 = "jabłko, pomarańcza, kiwi"
            eval_res4 = gemini_client.evaluate_answer(q4, a4_correct, user_ans_q4)
            print(f"Q: {q4}, Correct: {a4_correct}, User: '{user_ans_q4}' -> AI Correct: {eval_res4.is_correct}, Explanation: {eval_res4.explanation}")


        except ValueError as e:
            print(f"Initialization error: {e}")
        except RuntimeError as e:
            print(f"Runtime error during Gemini client test: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during Gemini client test: {e}")