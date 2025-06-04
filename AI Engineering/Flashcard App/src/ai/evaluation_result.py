# Relative path: src/ai/evaluation_result.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class EvaluationResult:
    """
    Represents the result of an AI evaluation for a flashcard answer.

    Attributes:
        is_correct (bool): True if the user's answer is considered correct, False otherwise.
        explanation (Optional[str]): An explanation from the AI, typically provided
                                     when the answer is incorrect.
    """
    is_correct: bool
    explanation: Optional[str] = None