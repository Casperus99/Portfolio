import logging
from abc import ABC, abstractmethod

# Set up logging for this module
logger = logging.getLogger(__name__)

class AIClientInterface(ABC):
    """
    Abstract Base Class (ABC) defining the interface for AI clients.
    Any AI client implementation (e.g., Gemini, OpenAI) must adhere to this interface.
    This promotes loose coupling and allows for easy swapping of AI providers.
    """

    @abstractmethod
    def evaluate_answer(self, question_front: str, correct_back: str, user_answer: str) -> bool:
        """
        Evaluates a user's answer against the correct answer using an AI model.

        The AI should assess the user's answer based on semantic meaning and presence of key information
        relative to the correct answer.

        Args:
            question_front (str): The question text from the flashcard.
            correct_back (str): The correct answer text from the flashcard.
            user_answer (str): The user's provided answer.

        Returns:
            bool: True if the AI considers the user's answer correct, False otherwise.
        """
        pass # Abstract methods do not have an implementation in the base class

# Example usage (for demonstration, not executable directly)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # Basic logging for example

    class MockAIClient(AIClientInterface):
        """A mock implementation for testing purposes."""
        def evaluate_answer(self, question_front: str, correct_back: str, user_answer: str) -> bool:
            logger.info(f"Mock AI evaluating: Q='{question_front}', Correct='{correct_back}', User='{user_answer}'")
            # Simple mock logic: correct if user answer contains 'correct' or matches correct_back
            if "correct" in user_answer.lower() or user_answer.lower() == correct_back.lower():
                return True
            return False

    mock_client = MockAIClient()
    print(f"Mock AI result 1: {mock_client.evaluate_answer('What is 2+2?', '4', '4')}")
    print(f"Mock AI result 2: {mock_client.evaluate_answer('Who was Einstein?', 'Physicist', 'He was a physicist')}")
    print(f"Mock AI result 3: {mock_client.evaluate_answer('Capital of France?', 'Paris', 'Lyon')}")