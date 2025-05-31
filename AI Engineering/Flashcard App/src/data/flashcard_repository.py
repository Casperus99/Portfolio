import json
import logging
from datetime import date
from pathlib import Path
from typing import List, Dict

from src.data.flashcard import Flashcard # Import Flashcard from the same package

# Set up logging for this module
logger = logging.getLogger(__name__)

class FlashcardRepository:
    """
    Manages loading and saving flashcards from/to JSON files.
    Responsible for handling file I/O, JSON parsing, and basic data validation.
    """

    def __init__(self) -> None:
        """
        Initializes the FlashcardRepository.
        No specific state needs to be maintained here, as it's primarily a stateless I/O handler.
        """
        logger.info("FlashcardRepository initialized.")

    def load_flashcards_from_directory(self, directory_path: Path) -> List[Flashcard]:
        """
        Recursively loads all flashcards from JSON files within the specified directory.
        Assigns UUIDs if missing and extracts category/deck information.

        Args:
            directory_path (Path): The base directory where flashcard JSON files are located.

        Returns:
            List[Flashcard]: A list of loaded Flashcard objects.

        Raises:
            FileNotFoundError: If the specified directory does not exist.
            json.JSONDecodeError: If a JSON file is malformed.
            ValueError: If a flashcard entry in a JSON file is missing required data or has invalid types.
            Exception: For other unexpected I/O errors.
        """
        if not directory_path.is_dir():
            logger.error(f"Flashcards directory not found: {directory_path}")
            raise FileNotFoundError(f"Flashcards directory not found: {directory_path}")

        all_flashcards: List[Flashcard] = []
        json_files_found = False

        logger.info(f"Scanning directory '{directory_path}' for flashcard JSON files...")

        # Use rglob to find all .json files recursively
        for json_file_path in directory_path.rglob('*.json'):
            json_files_found = True
            logger.debug(f"Found JSON file: {json_file_path}")
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if not isinstance(data, list):
                    logger.error(f"JSON file '{json_file_path}' does not contain a list of flashcards. Skipping.")
                    continue

                for i, item in enumerate(data):
                    if not isinstance(item, dict):
                        logger.warning(f"Item at index {i} in '{json_file_path}' is not a dictionary. Skipping.")
                        continue
                    try:
                        # Pass source_file_path and base_flashcards_dir for category/deck determination
                        flashcard = Flashcard.from_dict(item, json_file_path, directory_path)
                        all_flashcards.append(flashcard)
                    except ValueError as e:
                        logger.error(f"Error loading flashcard from '{json_file_path}' at index {i}: {e}")
                        # As per requirements, raise an error for malformed data
                        raise ValueError(f"Malformed flashcard data in '{json_file_path}' at index {i}: {e}") from e
                    except Exception as e:
                        logger.error(f"Unexpected error processing flashcard from '{json_file_path}' at index {i}: {e}")
                        raise # Re-raise unexpected errors

            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from '{json_file_path}': {e}")
                raise json.JSONDecodeError(f"Malformed JSON file: {json_file_path}. Error: {e}", e.doc, e.pos) from e
            except IOError as e:
                logger.error(f"Error reading file '{json_file_path}': {e}")
                raise IOError(f"Could not read file: {json_file_path}. Error: {e}") from e
            except Exception as e:
                logger.error(f"An unexpected error occurred while processing '{json_file_path}': {e}")
                raise

        if not json_files_found:
            logger.warning(f"No JSON files found in '{directory_path}'.")

        logger.info(f"Successfully loaded {len(all_flashcards)} flashcards from '{directory_path}'.")
        return all_flashcards

    def save_flashcards(self, flashcards: List[Flashcard]) -> None:
        """
        Saves a list of Flashcard objects back to their respective source JSON files.
        Flashcards are grouped by their 'source_file_path' attribute.

        Args:
            flashcards (List[Flashcard]): The list of Flashcard objects to save.

        Raises:
            IOError: If there is an error writing to a file.
            Exception: For other unexpected errors during saving.
        """
        # Group flashcards by their source file path
        flashcards_by_file: Dict[Path, List[dict]] = {}
        for fc in flashcards:
            if fc.source_file_path not in flashcards_by_file:
                flashcards_by_file[fc.source_file_path] = []
            flashcards_by_file[fc.source_file_path].append(fc.to_dict())

        logger.info(f"Attempting to save changes to {len(flashcards_by_file)} JSON files.")

        for file_path, fc_dicts in flashcards_by_file.items():
            try:
                # Ensure the directory exists before writing
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(fc_dicts, f, indent=2, ensure_ascii=False)
                logger.debug(f"Successfully saved {len(fc_dicts)} flashcards to '{file_path}'.")
            except IOError as e:
                logger.error(f"Error writing to file '{file_path}': {e}")
                raise IOError(f"Could not save flashcards to file: {file_path}. Error: {e}") from e
            except Exception as e:
                logger.error(f"An unexpected error occurred while saving to '{file_path}': {e}")
                raise
        logger.info("All flashcard changes saved successfully.")