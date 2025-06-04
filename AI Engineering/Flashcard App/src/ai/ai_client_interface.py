# Relative path: src/ai/ai_client_interface.py
import logging
from abc import ABC, abstractmethod
from typing import Optional

from src.ai.evaluation_result import EvaluationResult # Import the new result class

# Set up logging for this module
logger = logging.getLogger(__name__)

class AIClientInterface(ABC):
    """
    Abstract Base Class (ABC) defining the interface for AI clients.
    Any AI client implementation (e.g., Gemini, OpenAI) must adhere to this interface.
    This promotes loose coupling and allows for easy swapping of AI providers.
    """

    @abstractmethod
    def evaluate_answer(
        self,
        question_front: str,
        correct_back: str,
        user_answer: str,
        evaluation_hint: Optional[str] = None
    ) -> EvaluationResult: # Changed return type
        """
        Evaluates a user's answer against the correct answer using an AI model.

        The AI should assess the user's answer based on semantic meaning and presence of key information
        relative to the correct answer. An optional evaluation_hint can be provided to guide the AI.
        The method should return an EvaluationResult object containing the correctness
        and an optional explanation.

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
        pass # Abstract methods do not have an implementation in the base class

# Example usage (for demonstration, not executable directly)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # Basic logging for example

    class MockAIClient(AIClientInterface):
        """A mock implementation for testing purposes."""
        def evaluate_answer(
            self,
            question_front: str,
            correct_back: str,
            user_answer: str,
            evaluation_hint: Optional[str] = None
        ) -> EvaluationResult:
            logger.info(f"Mock AI evaluating: Q='{question_front}', Correct='{correct_back}', User='{user_answer}', Hint='{evaluation_hint}'")
            
            is_correct_val = False
            explanation_val = None

            if "correct" in user_answer.lower() or user_answer.lower() == correct_back.lower():
                is_correct_val = True
            else:
                explanation_val = "Mock explanation: Your answer was not deemed correct by the mock AI."
                if evaluation_hint and "strict" in evaluation_hint.lower():
                    if user_answer == correct_back:
                        is_correct_val = True
                        explanation_val = None
                    else:
                        is_correct_val = False
                        explanation_val = "Mock strict explanation: Answer did not exactly match."
            
            return EvaluationResult(is_correct=is_correct_val, explanation=explanation_val)

    mock_client = MockAIClient()
    res1 = mock_client.evaluate_answer('What is 2+2?', '4', '4')
    print(f"Mock AI result 1: Correct: {res1.is_correct}, Explanation: {res1.explanation}")
    
    res2 = mock_client.evaluate_answer('Who was Einstein?', 'Physicist', 'A scientist', evaluation_hint='Be lenient')
    print(f"Mock AI result 2: Correct: {res2.is_correct}, Explanation: {res2.explanation}")

    res3 = mock_client.evaluate_answer('Capital of France?', 'Paris', 'paris', evaluation_hint='Strict case matching')
    print(f"Mock AI result 3: Correct: {res3.is_correct}, Explanation: {res3.explanation}")

    res4 = mock_client.evaluate_answer('Capital of France?', 'Paris', 'Paris', evaluation_hint='Strict case matching')
    print(f"Mock AI result 4: Correct: {res4.is_correct}, Explanation: {res4.explanation}")