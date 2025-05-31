import logging
import json
from datetime import date, timedelta
from typing import Dict, List

from src.core.config_manager import ConfigManager
from src.data.flashcard import Flashcard

# Set up logging for this module
logger = logging.getLogger(__name__)

class SRSManager:
    """
    Manages the Spaced Repetition System (SRS) logic for flashcards.
    Determines which flashcards are due for review and updates their mastery levels.
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        """
        Initializes the SRSManager with access to application configuration.

        Args:
            config_manager (ConfigManager): An instance of ConfigManager to retrieve SRS intervals.
        """
        self._srs_intervals: Dict[int, int] = config_manager.get_srs_intervals()
        # Determine min and max mastery levels from the loaded intervals
        self._min_mastery_level: int = min(self._srs_intervals.keys()) if self._srs_intervals else 0
        self._max_mastery_level: int = max(self._srs_intervals.keys()) if self._srs_intervals else 6
        logger.info(f"SRSManager initialized with intervals: {self._srs_intervals}")
        logger.info(f"Min mastery level: {self._min_mastery_level}, Max mastery level: {self._max_mastery_level}")

        if not self._srs_intervals:
            logger.warning("SRS intervals are not configured. Using default values (0:0, 1:1, ...).")
            self._srs_intervals = {0: 0, 1: 1, 2: 2, 3: 4, 4: 7, 5: 12, 6: 20}
            self._min_mastery_level = 0
            self._max_mastery_level = 6

    def get_due_flashcards(self, all_flashcards: List[Flashcard], current_date: date) -> List[Flashcard]:
        """
        Filters a list of flashcards to return only those that are due for review
        on the given current_date according to the SRS intervals.

        Args:
            all_flashcards (List[Flashcard]): A list of all flashcards in the system.
            current_date (date): The current date to check against (e.g., date.today()).

        Returns:
            List[Flashcard]: A list of Flashcard objects that are due for review.
        """
        due_flashcards: List[Flashcard] = []
        for flashcard in all_flashcards:
            # Flashcards with mastery_level 0 are always due (same day)
            if flashcard.mastery_level == self._min_mastery_level:
                due_flashcards.append(flashcard)
                continue

            # If last_answer_date is not set, it's a new card or never answered, so it's due
            if flashcard.last_answer_date is None:
                due_flashcards.append(flashcard)
                continue

            # Calculate the next review date based on mastery level and intervals
            interval = self._srs_intervals.get(flashcard.mastery_level, self._max_srs_interval())
            next_review_date = flashcard.last_answer_date + timedelta(days=interval)

            if current_date >= next_review_date:
                due_flashcards.append(flashcard)
                logger.debug(f"Flashcard ID {flashcard.id} is due. Next review date: {next_review_date}")
            else:
                logger.debug(f"Flashcard ID {flashcard.id} is not yet due. Next review date: {next_review_date}")

        logger.info(f"Found {len(due_flashcards)} flashcards due for review on {current_date}.")
        return due_flashcards

    def update_mastery_level(self, flashcard: Flashcard, is_correct: bool, current_date: date) -> None:
        """
        Updates the mastery level and last answer date of a flashcard based on
        whether the user's answer was correct or incorrect.

        Args:
            flashcard (Flashcard): The flashcard object to update.
            is_correct (bool): True if the user's answer was correct, False otherwise.
            current_date (date): The date when the flashcard was answered.
        """
        if is_correct:
            # Increase mastery level, but not beyond the maximum defined level
            new_level = min(flashcard.mastery_level + 1, self._max_mastery_level)
            if new_level > flashcard.mastery_level:
                logger.debug(f"Flashcard ID {flashcard.id}: Mastery level increased from {flashcard.mastery_level} to {new_level}.")
            else:
                logger.debug(f"Flashcard ID {flashcard.id}: Mastery level already at max ({self._max_mastery_level}). No change.")
            flashcard.mastery_level = new_level
        else:
            # Decrease mastery level, but not below the minimum defined level (0)
            new_level = max(flashcard.mastery_level - 1, self._min_mastery_level)
            if new_level < flashcard.mastery_level:
                logger.debug(f"Flashcard ID {flashcard.id}: Mastery level decreased from {flashcard.mastery_level} to {new_level}.")
            else:
                logger.debug(f"Flashcard ID {flashcard.id}: Mastery level already at min ({self._min_mastery_level}). No change.")
            flashcard.mastery_level = new_level

        flashcard.last_answer_date = current_date
        logger.info(f"Flashcard ID {flashcard.id} updated. New level: {flashcard.mastery_level}, Last answered: {flashcard.last_answer_date}.")

    def get_mastery_distribution(self, all_flashcards: List[Flashcard]) -> Dict[int, int]:
        """
        Calculates the distribution of flashcards across different mastery levels.

        Args:
            all_flashcards (List[Flashcard]): A list of all flashcards in the system.

        Returns:
            Dict[int, int]: A dictionary where keys are mastery levels and values are
                            the count of flashcards at that level. Includes all levels
                            from min to max, even if count is 0.
        """
        distribution: Dict[int, int] = {level: 0 for level in range(self._min_mastery_level, self._max_mastery_level + 1)}
        for flashcard in all_flashcards:
            # Ensure the level is within the expected range, default to min if somehow out of bounds
            level = max(self._min_mastery_level, min(flashcard.mastery_level, self._max_mastery_level))
            distribution[level] += 1
        logger.debug(f"Calculated mastery distribution: {distribution}")
        return distribution

    def _max_srs_interval(self) -> int:
        """Helper to get the maximum interval defined in the configuration."""
        return max(self._srs_intervals.values()) if self._srs_intervals else 20 # Default if config is empty

# Example usage (for testing, will be called from main.py)
if __name__ == '__main__':
    from src.core.logger_setup import setup_logging
    from src.core.config_manager import ConfigManager
    from src.data.flashcard import Flashcard
    from pathlib import Path
    from uuid import uuid4

    setup_logging('DEBUG')

    # Setup a dummy config manager for testing
    dummy_config_path = Path('test_srs_config.json')
    dummy_config_content = {
        "srs_intervals": {
            "0": 0, "1": 1, "2": 2, "3": 4, "4": 7, "5": 12, "6": 20
        },
        "ai_settings": {"api_key": "dummy", "model_name": "dummy"},
        "flashcards_directory": "dummy"
    }
    with open(dummy_config_path, 'w', encoding='utf-8') as f:
        json.dump(dummy_config_content, f, indent=2)

    config_manager = ConfigManager()
    config_manager.load_config(dummy_config_path)

    srs_manager = SRSManager(config_manager)

    today = date.today()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    five_days_ago = today - timedelta(days=5)

    # Create some dummy flashcards
    fc1 = Flashcard(id=uuid4(), front="Question 1", back="Answer 1", mastery_level=0, last_answer_date=yesterday, category="test", deck="deck1", source_file_path=Path("dummy/deck1.json"))
    fc2 = Flashcard(id=uuid4(), front="Question 2", back="Answer 2", mastery_level=1, last_answer_date=yesterday, category="test", deck="deck1", source_file_path=Path("dummy/deck1.json")) # Due today
    fc3 = Flashcard(id=uuid4(), front="Question 3", back="Answer 3", mastery_level=2, last_answer_date=two_days_ago, category="test", deck="deck2", source_file_path=Path("dummy/deck2.json")) # Due today
    fc4 = Flashcard(id=uuid4(), front="Question 4", back="Answer 4", mastery_level=3, last_answer_date=two_days_ago, category="test", deck="deck2", source_file_path=Path("dummy/deck2.json")) # Not due (interval 4)
    fc5 = Flashcard(id=uuid4(), front="Question 5", back="Answer 5", mastery_level=0, last_answer_date=None, category="test", deck="deck3", source_file_path=Path("dummy/deck3.json")) # New card, always due
    fc6 = Flashcard(id=uuid4(), front="Question 6", back="Answer 6", mastery_level=6, last_answer_date=five_days_ago, category="test", deck="deck3", source_file_path=Path("dummy/deck3.json")) # Not due (interval 20)

    all_test_flashcards = [fc1, fc2, fc3, fc4, fc5, fc6]

    # Test get_due_flashcards
    print(f"\n--- Testing get_due_flashcards for {today} ---")
    due_cards = srs_manager.get_due_flashcards(all_test_flashcards, today)
    print(f"Due flashcards ({len(due_cards)}):")
    for fc in due_cards:
        print(f"  - ID: {fc.id}, Front: '{fc.front}', Level: {fc.mastery_level}, Last Answer: {fc.last_answer_date}")
    # Expected: fc1 (level 0), fc2 (level 1, answered yesterday, interval 1), fc3 (level 2, answered 2 days ago, interval 2), fc5 (new)

    # Test update_mastery_level
    print("\n--- Testing update_mastery_level ---")
    print(f"Before update: fc1 mastery={fc1.mastery_level}, last_answer_date={fc1.last_answer_date}")
    srs_manager.update_mastery_level(fc1, True, today) # Correct
    print(f"After correct update: fc1 mastery={fc1.mastery_level}, last_answer_date={fc1.last_answer_date}")
    # Expected: level 1, today

    print(f"Before update: fc2 mastery={fc2.mastery_level}, last_answer_date={fc2.last_answer_date}")
    srs_manager.update_mastery_level(fc2, False, today) # Incorrect
    print(f"After incorrect update: fc2 mastery={fc2.mastery_level}, last_answer_date={fc2.last_answer_date}")
    # Expected: level 0, today

    print(f"Before update: fc6 mastery={fc6.mastery_level}, last_answer_date={fc6.last_answer_date}")
    srs_manager.update_mastery_level(fc6, True, today) # Correct, already max level
    print(f"After correct update (max level): fc6 mastery={fc6.mastery_level}, last_answer_date={fc6.last_answer_date}")
    # Expected: level 6, today

    # Test get_mastery_distribution
    print("\n--- Testing get_mastery_distribution ---")
    # Update some levels for a more interesting distribution
    srs_manager.update_mastery_level(fc4, True, today) # Level 3 -> 4
    srs_manager.update_mastery_level(fc5, True, today) # Level 0 -> 1

    current_distribution = srs_manager.get_mastery_distribution(all_test_flashcards)
    print(f"Current mastery distribution: {current_distribution}")
    # Expected: {0: 1 (fc2), 1: 2 (fc1, fc5), 2: 1 (fc3), 3: 0, 4: 1 (fc4), 5: 0, 6: 1 (fc6)}

    # Clean up dummy config file
    if dummy_config_path.exists():
        dummy_config_path.unlink()