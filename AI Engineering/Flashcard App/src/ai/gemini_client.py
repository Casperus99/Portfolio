import logging
import os
from typing import Optional

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

from src.ai.ai_client_interface import AIClientInterface

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

    def evaluate_answer(self, question_front: str, correct_back: str, user_answer: str) -> bool:
        """
        Evaluates a user's answer against the correct answer using the Gemini AI model.

        The AI assesses the user's answer based on semantic meaning and presence of key information
        relative to the correct answer. The evaluation prompt guides the AI to respond with
        a simple "YES" or "NO".

        Args:
            question_front (str): The question text from the flashcard.
            correct_back (str): The correct answer text from the flashcard.
            user_answer (str): The user's provided answer.

        Returns:
            bool: True if the AI considers the user's answer correct, False otherwise.
        """
        if not self._model:
            logger.error("Gemini model is not initialized. Cannot evaluate answer.")
            return False

        prompt = (
            f"Given the following flashcard question and its correct answer, "
            f"determine if the user's answer is correct.\n"
            f"Consider semantic similarity and the presence of key information. "
            f"Respond ONLY with 'YES' if the answer is correct, and 'NO' if it is incorrect.\n\n"
            f"Question: {question_front}\n"
            f"Correct Answer: {correct_back}\n"
            f"User's Answer: {user_answer}\n\n"
            f"Is the user's answer correct? (YES/NO):"
        )
        logger.debug(f"Sending prompt to Gemini: {prompt}")

        try:
            # Configure safety settings to potentially reduce false positives/negatives related to content
            # These are examples and might need fine-tuning based on actual model behavior.
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
                    temperature=0.0,  # Aim for deterministic output
                    max_output_tokens=5 # Expecting 'YES' or 'NO'
                )
            )
            # Accessing text from parts of the response
            # Check if response.parts exists and has content
            if response.parts and response.parts[0].text:
                ai_response_text = response.parts[0].text.strip().upper()
                logger.debug(f"Gemini raw response: '{ai_response_text}'")
                return ai_response_text == "YES"
            else:
                logger.warning(f"Gemini returned empty or unparseable response for question ID: {question_front}. Assuming incorrect.")
                return False

        except genai.types.BlockedPromptException as e:
            logger.error(f"Gemini API blocked the prompt due to safety reasons: {e}")
            logger.error(f"Prompt content: {prompt}")
            return False
        except Exception as e:
            logger.error(f"An error occurred during Gemini API call: {e}")
            return False

# Example usage (requires an actual API key to run successfully)
if __name__ == '__main__':
    from src.core.logger_setup import setup_logging
    setup_logging('DEBUG')

    # IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with a real API key for testing
    # You can set it as an environment variable or directly here for testing.
    # For production, always use environment variables or a secure configuration.
    gemini_api_key = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

    if gemini_api_key == "YOUR_GEMINI_API_KEY":
        logger.warning("Please set the GEMINI_API_KEY environment variable or replace 'YOUR_GEMINI_API_KEY' in the test.")
        print("Skipping GeminiClient direct test due to missing API key.")
    else:
        try:
            gemini_client = GeminiClient(api_key=gemini_api_key, model_name="gemini-1.5-flash")

            print("\n--- Testing GeminiClient ---")
            q1 = "What is the capital of France?"
            a1_correct = "Paris"
            a1_user_correct = "It's Paris"
            a1_user_incorrect = "London"
            a1_user_semantically_correct = "The city of lights, Paris"

            print(f"Q: {q1}, Correct: {a1_correct}, User: '{a1_user_correct}' -> Correct? {gemini_client.evaluate_answer(q1, a1_correct, a1_user_correct)}")
            print(f"Q: {q1}, Correct: {a1_correct}, User: '{a1_user_incorrect}' -> Correct? {gemini_client.evaluate_answer(q1, a1_correct, a1_user_incorrect)}")
            print(f"Q: {q1}, Correct: {a1_correct}, User: '{a1_user_semantically_correct}' -> Correct? {gemini_client.evaluate_answer(q1, a1_correct, a1_user_semantically_correct)}")

            q2 = "When was World War II?"
            a2_correct = "1939-1945"
            a2_user_correct = "From 1939 to 1945"
            a2_user_incorrect = "1914-1918"

            print(f"Q: {q2}, Correct: {a2_correct}, User: '{a2_user_correct}' -> Correct? {gemini_client.evaluate_answer(q2, a2_correct, a2_user_correct)}")
            print(f"Q: {q2}, Correct: {a2_correct}, User: '{a2_user_incorrect}' -> Correct? {gemini_client.evaluate_answer(q2, a2_correct, a2_user_incorrect)}")

        except ValueError as e:
            print(f"Initialization error: {e}")
        except RuntimeError as e:
            print(f"Runtime error during Gemini client test: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during Gemini client test: {e}")