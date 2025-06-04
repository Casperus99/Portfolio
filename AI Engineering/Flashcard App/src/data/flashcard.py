# Relative path: src/data/flashcard.py
import logging
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Optional
from uuid import UUID, uuid4

# Set up logging for this module
logger = logging.getLogger(__name__)


@dataclass
class Flashcard:
    """
    Represents a single flashcard with its question, answer, and SRS metadata.
    Includes metadata about its origin file for persistence and an optional evaluation hint.
    """
    # Fields without default values must come first
    front: str
    back: str
    source_file_path: Path = field(compare=False, repr=False) # Full path to the original JSON file

    # Fields with default values can follow
    id: UUID = field(default_factory=uuid4)
    mastery_level: int = 0
    last_answer_date: Optional[date] = None
    category: str = "default"  # Name of the subfolder (e.g., "Zdrowie")
    deck: str = "default"      # Name of the JSON file (e.g., "owoce")
    evaluation_hint: Optional[str] = None # Optional hint for the AI evaluator

    def __post_init__(self) -> None:
        """
        Post-initialization validation for Flashcard attributes.
        Ensures mastery_level is within a valid range.
        """
        if not (0 <= self.mastery_level <= 6): # Assuming max level 6 based on typical SRS
            logger.warning(f"Flashcard ID {self.id}: Mastery level {self.mastery_level} is out of expected range (0-6). Clamping.")
            self.mastery_level = max(0, min(self.mastery_level, 6))

    @classmethod
    def from_dict(cls, data: dict, source_file_path: Path, base_flashcards_dir: Path) -> 'Flashcard':
        """
        Creates a Flashcard instance from a dictionary (e.g., loaded from JSON).

        Args:
            data (dict): The dictionary containing flashcard data.
            source_file_path (Path): The full path to the JSON file this flashcard came from.
            base_flashcards_dir (Path): The base directory for all flashcards (e.g., 'flashcards/').

        Returns:
            Flashcard: An initialized Flashcard object.

        Raises:
            ValueError: If essential flashcard data is missing or malformed.
        """
        # Validate required fields
        if 'front' not in data or not isinstance(data['front'], str):
            raise ValueError("Flashcard 'front' (question) is missing or not a string.")
        if 'back' not in data or not isinstance(data['back'], str):
            raise ValueError("Flashcard 'back' (answer) is missing or not a string.")

        # Parse ID
        flashcard_id = uuid4()
        if 'id' in data and data['id'] is not None:
            try:
                flashcard_id = UUID(data['id'])
            except ValueError as e:
                logger.warning(f"Invalid UUID format for ID '{data['id']}' in file {source_file_path}. Generating new UUID. Error: {e}")
                # Keep the default_factory uuid4() if parsing fails

        # Parse mastery_level
        mastery_level = 0
        if 'mastery_level' in data and data['mastery_level'] is not None:
            try:
                mastery_level = int(data['mastery_level'])
            except (ValueError, TypeError):
                logger.warning(f"Invalid mastery_level '{data['mastery_level']}' for flashcard ID {flashcard_id} in file {source_file_path}. Defaulting to 0.")
                mastery_level = 0

        # Parse last_answer_date
        last_answer_date = None
        if 'last_answer_date' in data and data['last_answer_date'] is not None:
            try:
                last_answer_date = date.fromisoformat(data['last_answer_date'])
            except ValueError:
                logger.warning(f"Invalid date format '{data['last_answer_date']}' for flashcard ID {flashcard_id} in file {source_file_path}. Setting last_answer_date to None.")
                last_answer_date = None

        # Determine category and deck from source_file_path relative to base_flashcards_dir
        try:
            relative_path = source_file_path.relative_to(base_flashcards_dir)
            # Category is the name of the parent directory of the JSON file, relative to base_flashcards_dir
            # If the JSON file is directly in base_flashcards_dir, its parent relative to base is '.'
            category_parts = [part for part in relative_path.parent.parts if part != '.']
            category = "/".join(category_parts) if category_parts else "root"
            deck = source_file_path.stem
        except ValueError:
            logger.warning(
                f"Could not determine category/deck for {source_file_path} relative to {base_flashcards_dir}. "
                "Using 'unknown' for category and deck."
            )
            category = "unknown"
            deck = source_file_path.stem

        # Parse evaluation_hint (optional)
        evaluation_hint_data = data.get('evaluation_hint')
        evaluation_hint: Optional[str] = None
        if evaluation_hint_data is not None:
            if isinstance(evaluation_hint_data, str):
                evaluation_hint = evaluation_hint_data
            else:
                logger.warning(f"Invalid type for 'evaluation_hint' (expected string, got {type(evaluation_hint_data)}) for flashcard ID {flashcard_id} in file {source_file_path}. Ignoring hint.")

        return cls(
            id=flashcard_id,
            front=data['front'],
            back=data['back'],
            mastery_level=mastery_level,
            last_answer_date=last_answer_date,
            category=category,
            deck=deck,
            source_file_path=source_file_path,
            evaluation_hint=evaluation_hint # Assign parsed hint
        )

    def to_dict(self) -> dict:
        """
        Converts the Flashcard instance to a dictionary suitable for JSON serialization.
        Excludes category, deck, and source_file_path as they are derived metadata for saving.
        Includes evaluation_hint if it's set.
        """
        data_dict = {
            "id": str(self.id),
            "front": self.front,
            "back": self.back,
            "mastery_level": self.mastery_level,
            "last_answer_date": self.last_answer_date.isoformat() if self.last_answer_date else None,
        }
        if self.evaluation_hint is not None:
            data_dict["evaluation_hint"] = self.evaluation_hint
        return data_dict

# Example usage (for testing, will be called from main.py or other test files)
if __name__ == '__main__':
    from src.core.logger_setup import setup_logging
    setup_logging({'log_level': 'DEBUG', 'log_to_console': True, 'log_to_file': False, 'log_file_path': '', 'clear_log_on_start': False})

    base_dir = Path("flashcards_test_data")
    source_file = base_dir / "CategoryA" / "Deck1.json"
    source_file_root = base_dir / "RootDeck.json"

    # Test data
    flashcard_data_with_hint = {
        "id": str(uuid4()),
        "front": "What is 2+2?",
        "back": "4",
        "mastery_level": 1,
        "last_answer_date": "2023-01-01",
        "evaluation_hint": "Expect a numerical answer only."
    }
    flashcard_data_no_hint = {
        "id": str(uuid4()),
        "front": "Capital of France?",
        "back": "Paris",
        "mastery_level": 0,
        "last_answer_date": None
    }
    flashcard_data_invalid_hint = {
        "id": str(uuid4()),
        "front": "Is Python fun?",
        "back": "Yes",
        "evaluation_hint": 123 # Invalid type
    }
    flashcard_data_root_deck = {
        "id": str(uuid4()),
        "front": "Root Question",
        "back": "Root Answer",
        "evaluation_hint": "Root hint"
    }


    # Test from_dict
    fc1 = Flashcard.from_dict(flashcard_data_with_hint, source_file, base_dir)
    fc2 = Flashcard.from_dict(flashcard_data_no_hint, source_file, base_dir)
    fc3 = Flashcard.from_dict(flashcard_data_invalid_hint, source_file, base_dir) # Should log warning
    fc4 = Flashcard.from_dict(flashcard_data_root_deck, source_file_root, base_dir)


    print("--- Flashcard 1 (with hint) ---")
    print(f"ID: {fc1.id}, Front: '{fc1.front}', Hint: '{fc1.evaluation_hint}'")
    print(f"Category: {fc1.category}, Deck: {fc1.deck}")
    print(f"Serialized: {fc1.to_dict()}")

    print("\n--- Flashcard 2 (no hint) ---")
    print(f"ID: {fc2.id}, Front: '{fc2.front}', Hint: '{fc2.evaluation_hint}'")
    print(f"Category: {fc2.category}, Deck: {fc2.deck}")
    print(f"Serialized: {fc2.to_dict()}")

    print("\n--- Flashcard 3 (invalid hint) ---")
    print(f"ID: {fc3.id}, Front: '{fc3.front}', Hint: '{fc3.evaluation_hint}'") # Hint should be None
    print(f"Category: {fc3.category}, Deck: {fc3.deck}")
    print(f"Serialized: {fc3.to_dict()}") # Hint should not be in dict

    print("\n--- Flashcard 4 (root deck) ---")
    print(f"ID: {fc4.id}, Front: '{fc4.front}', Hint: '{fc4.evaluation_hint}'")
    print(f"Category: {fc4.category}, Deck: {fc4.deck}") # Category should be 'root'
    print(f"Serialized: {fc4.to_dict()}")

    # Test default values
    default_fc = Flashcard(front="Default Q", back="Default A", source_file_path=source_file)
    print("\n--- Default Flashcard ---")
    print(f"ID: {default_fc.id}, Front: '{default_fc.front}', Hint: '{default_fc.evaluation_hint}'")
    print(f"Serialized: {default_fc.to_dict()}")