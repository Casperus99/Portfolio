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
    Includes metadata about its origin file for persistence.
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

    def __post_init__(self) -> None:
        """
        Post-initialization validation for Flashcard attributes.
        Ensures mastery_level is within a valid range.
        """
        if not (0 <= self.mastery_level <= 6):
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
            category = relative_path.parent.name if relative_path.parent.name else "root"
            deck = source_file_path.stem
        except ValueError:
            # This can happen if source_file_path is not under base_flashcards_dir
            logger.warning(
                f"Could not determine category/deck for {source_file_path} relative to {base_flashcards_dir}. "
                "Using 'unknown' for category and deck."
            )
            category = "unknown"
            deck = source_file_path.stem


        return cls(
            id=flashcard_id,
            front=data['front'],
            back=data['back'],
            mastery_level=mastery_level,
            last_answer_date=last_answer_date,
            category=category,
            deck=deck,
            source_file_path=source_file_path
        )

    def to_dict(self) -> dict:
        """
        Converts the Flashcard instance to a dictionary suitable for JSON serialization.
        Excludes category, deck, and source_file_path as they are derived metadata for saving.
        """
        return {
            "id": str(self.id),
            "front": self.front,
            "back": self.back,
            "mastery_level": self.mastery_level,
            "last_answer_date": self.last_answer_date.isoformat() if self.last_answer_date else None,
        }