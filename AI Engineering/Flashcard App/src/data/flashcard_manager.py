import logging
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from src.data.flashcard import Flashcard
from src.data.flashcard_repository import FlashcardRepository

# Set up logging for this module
logger = logging.getLogger(__name__)

class FlashcardManager:
    """
    Manages the collection of Flashcard objects in memory.
    Delegates persistence operations (loading/saving) to a FlashcardRepository.
    """

    def __init__(self, repository: FlashcardRepository) -> None:
        """
        Initializes the FlashcardManager with a given repository.

        Args:
            repository (FlashcardRepository): An instance of FlashcardRepository for data persistence.
        """
        self._repository: FlashcardRepository = repository
        self._flashcards: List[Flashcard] = []  # Stores all loaded flashcards
        logger.info("FlashcardManager initialized.")

    def load_all_flashcards(self, directory_path: Path) -> None:
        """
        Loads all flashcards from the specified directory using the repository.

        Args:
            directory_path (Path): The base directory containing flashcard JSON files.

        Raises:
            FileNotFoundError: If the directory does not exist.
            json.JSONDecodeError: If a JSON file is malformed.
            ValueError: If flashcard data is invalid.
        """
        logger.info(f"Attempting to load all flashcards from '{directory_path}'.")
        self._flashcards = self._repository.load_flashcards_from_directory(directory_path)
        logger.info(f"Loaded {len(self._flashcards)} flashcards into manager.")

    def get_all_flashcards(self) -> List[Flashcard]:
        """
        Returns a list of all flashcards currently managed.

        Returns:
            List[Flashcard]: A list of Flashcard objects.
        """
        # Return a shallow copy to prevent external modification of the internal list
        return list(self._flashcards)

    def get_flashcard_by_id(self, flashcard_id: UUID) -> Optional[Flashcard]:
        """
        Retrieves a specific flashcard by its unique ID.

        Args:
            flashcard_id (UUID): The UUID of the flashcard to retrieve.

        Returns:
            Optional[Flashcard]: The Flashcard object if found, None otherwise.
        """
        for flashcard in self._flashcards:
            if flashcard.id == flashcard_id:
                logger.debug(f"Flashcard with ID {flashcard_id} found.")
                return flashcard
        logger.warning(f"Flashcard with ID {flashcard_id} not found.")
        return None

    def update_flashcard(self, updated_flashcard: Flashcard) -> None:
        """
        Updates an existing flashcard's data in the manager's collection.
        This method assumes the updated_flashcard object is the one that was retrieved
        from this manager and modified. If it's a new instance, it finds and replaces.

        Args:
            updated_flashcard (Flashcard): The Flashcard object with updated data.
        """
        found = False
        for i, fc in enumerate(self._flashcards):
            if fc.id == updated_flashcard.id:
                # Replace the old flashcard object with the updated one
                self._flashcards[i] = updated_flashcard
                found = True
                logger.debug(f"Flashcard with ID {updated_flashcard.id} updated in memory.")
                break
        if not found:
            logger.warning(f"Attempted to update flashcard with ID {updated_flashcard.id} but it was not found in manager's collection.")

    def save_all_flashcards(self) -> None:
        """
        Saves all managed flashcards back to their respective source JSON files
        using the repository.
        """
        logger.info("Initiating save of all flashcards via repository.")
        self._repository.save_flashcards(self._flashcards)
        logger.info("All flashcards save operation completed.")