import logging
import json # For handling potential JSONDecodeError from data layer
from datetime import date, timedelta # Added timedelta for mock repo
from pathlib import Path
import random # For shuffling flashcards
import sys # For sys.exit()
from typing import List

# Import core components for setup
from src.core.logger_setup import setup_logging
from src.core.config_manager import ConfigManager

# Import data layer components
from src.data.flashcard_repository import FlashcardRepository
from src.data.flashcard_manager import FlashcardManager

# Import SRS logic component
from src.srs.srs_manager import SRSManager

# Import AI integration component
from src.ai.gemini_client import GeminiClient # Specific client
from src.ai.ai_client_interface import AIClientInterface # Interface for type hinting

# Import UI component
from src.ui.terminal_ui import TerminalUI
from src.data.flashcard import Flashcard # To type hint flashcard objects

# Set up a logger for the main script (will be configured by setup_logging)
logger = logging.getLogger(__name__)

class Application:
    """
    The main application orchestrator for the Flashcards SRS system.
    Coordinates interactions between different components (data, SRS, AI, UI).
    """

    def __init__(
        self,
        config_manager: ConfigManager,
        flashcard_manager: FlashcardManager,
        srs_manager: SRSManager,
        ai_client: AIClientInterface,
        ui: TerminalUI
    ) -> None:
        """
        Initializes the Application with all its required dependencies.

        Args:
            config_manager (ConfigManager): Manages application configuration.
            flashcard_manager (FlashcardManager): Manages flashcard data.
            srs_manager (SRSManager): Manages the Spaced Repetition System logic.
            ai_client (AIClientInterface): Handles AI model interactions for answer evaluation.
            ui (TerminalUI): Manages user interface interactions in the terminal.
        """
        self._config_manager = config_manager
        self._flashcard_manager = flashcard_manager
        self._srs_manager = srs_manager
        self._ai_client = ai_client
        self._ui = ui
        self._running = True # Flag to control the main application loop
        logger.info("Application initialized.")

    def run(self) -> None:
        """
        Starts the main application loop.
        Handles loading data, running the quiz session, and saving progress.
        """
        logger.info("Application started.")
        self._ui.clear_screen()

        # 1. Load flashcards
        try:
            flashcards_dir_str = self._config_manager.get_setting('flashcards_directory')
            if not flashcards_dir_str:
                raise ValueError("Flashcards directory path is not configured in settings.json.")
            flashcards_dir = Path(flashcards_dir_str)
            self._flashcard_manager.load_all_flashcards(flashcards_dir)
        except (FileNotFoundError, json.JSONDecodeError, ValueError, IOError) as e:
            logger.critical(f"Failed to load flashcards: {e}. Exiting application.")
            self._ui.display_message(f"Błąd krytyczny: Nie udało się wczytać fiszek. {e}")
            return
        except Exception as e:
            logger.critical(f"An unexpected error occurred during flashcard loading: {e}. Exiting application.")
            self._ui.display_message(f"Wystąpił nieoczekiwany błąd podczas ładowania fiszek: {e}")
            return

        all_flashcards = self._flashcard_manager.get_all_flashcards()
        if not all_flashcards:
            self._ui.display_message("Brak fiszek w systemie. Dodaj pliki JSON do folderu 'flashcards/'.")
            logger.info("No flashcards found in the system. Exiting.")
            return

        # 2. Prepare session
        current_date = date.today()
        due_flashcards_for_session = self._srs_manager.get_due_flashcards(all_flashcards, current_date)
        random.shuffle(due_flashcards_for_session) # Shuffle for random question order

        if not due_flashcards_for_session:
            self._ui.display_message("Gratulacje! Na dziś nie ma więcej pytań do powtórki.")
            logger.info("No flashcards due for review today. Exiting.")
            return

        logger.info(f"Starting quiz session with {len(due_flashcards_for_session)} initially due flashcards.")

        # 3. Main quiz loop
        while self._running and due_flashcards_for_session:
            self._ui.clear_screen()
            mastery_dist = self._srs_manager.get_mastery_distribution(all_flashcards)
            # Display the current number of cards remaining in the due_flashcards_for_session list
            self._ui.display_stats(len(due_flashcards_for_session), mastery_dist)

            current_flashcard: Flashcard = due_flashcards_for_session[0] # Get the first card

            self._ui.display_question(current_flashcard)
            user_answer = self._ui.get_user_input("Twoja odpowiedź: ")

            if user_answer.lower() == self._ui.EXIT_KEY: # Check for 'q' case-insensitively
                self._running = False
                logger.info("User requested exit during input.")
                break # Exit the loop

            # Evaluate answer using AI
            logger.debug(f"Evaluating answer for flashcard ID: {current_flashcard.id}")
            is_correct = self._ai_client.evaluate_answer(
                current_flashcard.front,
                current_flashcard.back,
                user_answer
            )

            # Update SRS mastery level and last answer date
            self._srs_manager.update_mastery_level(current_flashcard, is_correct, current_date)
            # Update the flashcard in the manager's collection (important for saving)
            self._flashcard_manager.update_flashcard(current_flashcard)

            # Save progress after each answer
            try:
                self._flashcard_manager.save_all_flashcards()
                logger.info(f"Progress saved for flashcard ID: {current_flashcard.id}")
            except (IOError, Exception) as e:
                logger.error(f"Failed to save flashcard progress for ID {current_flashcard.id}: {e}")
                self._ui.display_message(f"Błąd zapisu postępów dla fiszki {current_flashcard.id}: {e}")
                # For now, we log and continue to allow user to finish session.

            # Display feedback and handle pause on the SAME SCREEN
            # Clear screen and re-display stats/question context to show updated stats
            self._ui.clear_screen()
            mastery_dist = self._srs_manager.get_mastery_distribution(all_flashcards) # Get updated stats
            # --- MODIFIED START ---
            # Decide if the card will be removed or re-added for the purpose of the 'available_count'
            # This is a temporary count for display before actual list modification.
            temp_available_count = len(due_flashcards_for_session)
            if is_correct:
                # If correct, it will be removed, so count decreases by 1 for the next display
                # unless it's the last card
                if temp_available_count > 0:
                    temp_available_count -=1
            else: # Incorrect
                if current_flashcard.mastery_level != self._srs_manager._min_mastery_level:
                    # If incorrect and NOT level 0, it will be removed
                    if temp_available_count > 0:
                        temp_available_count -=1
                # If incorrect AND level 0, it's re-added, so count effectively stays same for next display
                # (or seems to, as it's popped then appended)
            self._ui.display_stats(temp_available_count if temp_available_count >=0 else 0, mastery_dist)
            # --- MODIFIED END ---
            self._ui.display_question(current_flashcard) # Re-display question
            self._ui.display_user_answer(user_answer) # Re-display user's answer

            # Provide feedback to user
            if is_correct:
                self._ui.display_correct_answer_feedback() # Show "^^^ DOBRZE ^^^"
                self._ui.display_correct_answer_only(current_flashcard.back) # Show correct answer
                
                print() # Add empty line before the next wait prompt
                
                # Pause after correct answer, allow exit
                wait_input = self._ui.wait_for_key_press()
                if wait_input.lower() == self._ui.EXIT_KEY: # Check for 'q' case-insensitively
                    self._running = False
                    logger.info("User requested exit after correct answer.")
                    break # Exit the loop
                
                due_flashcards_for_session.pop(0) # Remove from the session's due list

            else: # Incorrect answer
                self._ui.display_incorrect_feedback_short() # First feedback: "###   ŹLE   ###"
                self._ui.display_correct_answer_only(current_flashcard.back) # Show correct answer
                print() # Add empty line before the next wait prompt
                
                # Single pause after "ŹLE." and correct answer
                wait_input = self._ui.wait_for_key_press()
                if wait_input.lower() == self._ui.EXIT_KEY: # Check for 'q' case-insensitively
                    self._running = False
                    logger.info("User requested exit after incorrect answer.")
                    break # Exit the loop

                # If incorrect and mastery level dropped to min (0),
                # move it to the end of due_flashcards_for_session.
                # Otherwise, remove it.
                if current_flashcard.mastery_level == self._srs_manager._min_mastery_level:
                    card_to_readd = due_flashcards_for_session.pop(0) # Remove from front
                    due_flashcards_for_session.append(card_to_readd) # Add to end
                    logger.debug(f"Flashcard ID {current_flashcard.id} moved to end of due list (level {current_flashcard.mastery_level}).")
                else:
                    due_flashcards_for_session.pop(0) # Remove from front as it's done for today


        # 4. End of session messages
        self._ui.clear_screen()
        if not self._running:
            self._ui.display_message("Zapisano postępy. Do zobaczenia!")
            logger.info("Application exited by user request.")
        else:
            self._ui.display_message("Koniec pytań w tym dniu. Postępy zostały zapisane.")
            logger.info("All due flashcards for today have been reviewed. Session ended.")

        logger.info("Application finished gracefully.")

# Example usage (for testing, will be called from main.py)
if __name__ == '__main__':
    # This block is for demonstrating how Application would be assembled and run.
    # It requires mock implementations of all its dependencies.
    # In a real scenario, these would be concrete classes.

    from src.core.logger_setup import setup_logging
    from src.core.config_manager import ConfigManager
    from src.data.flashcard import Flashcard
    from src.data.flashcard_repository import FlashcardRepository
    from src.ai.ai_client_interface import AIClientInterface
    from src.ui.terminal_ui import TerminalUI
    from uuid import uuid4
    import os
    import time # For mock UI delays

    # Configure logging for the test block (independent of app's config)
    setup_logging({
        'log_level': 'DEBUG',
        'log_to_console': True, # Keep console logging for this test
        'log_to_file': False,
        'log_file_path': 'test_app.log',
        'clear_log_on_start': True
    })

    # --- Mocks for testing Application class ---
    class MockConfigManager(ConfigManager):
        def __init__(self):
            super().__init__()
            self._config = {
                "srs_intervals": {"0": 0, "1": 1, "2": 2, "3": 4, "4": 7, "5": 12, "6": 20},
                "ai_settings": {"api_key": "mock_key", "model_name": "mock-model"},
                "flashcards_directory": "mock_flashcards/",
                "logging_settings": {"log_level": "INFO", "log_to_console": True, "log_to_file": False, "log_file_path": "app.log", "clear_log_on_start": False}
            }
            logger.debug("MockConfigManager initialized.")

    class MockFlashcardRepository(FlashcardRepository):
        def __init__(self):
            super().__init__()
            self._mock_data = [
                Flashcard(front="Mock Q1 (lvl0)", back="Mock A1", mastery_level=0, last_answer_date=None, category="mock", deck="test", source_file_path=Path("mock_flashcards/mock/test.json")),
                Flashcard(front="Mock Q2 (lvl1 due)", back="Mock A2", mastery_level=1, last_answer_date=date.today() - timedelta(days=1), category="mock", deck="test", source_file_path=Path("mock_flashcards/mock/test.json")),
                Flashcard(front="Mock Q3 (lvl2 due)", back="Mock A3", mastery_level=2, last_answer_date=date.today() - timedelta(days=2), category="mock", deck="test", source_file_path=Path("mock_flashcards/mock/test.json")),
            ]
            logger.debug("MockFlashcardRepository initialized.")

        def load_flashcards_from_directory(self, directory_path: Path) -> List[Flashcard]:
            logger.info(f"Mock loading flashcards from {directory_path}. Returning {len(self._mock_data)} mock cards.")
            return list(self._mock_data)

        def save_flashcards(self, flashcards: List[Flashcard]) -> None:
            logger.info(f"Mock saving {len(flashcards)} flashcards.")
            # In a real scenario, you'd update self._mock_data based on IDs
            for fc in flashcards:
                for i, mock_fc in enumerate(self._mock_data):
                    if mock_fc.id == fc.id:
                        self._mock_data[i] = fc # Replace with updated object
                        break
            logger.debug("Mock flashcards updated in repository.")

    class MockAIClient(AIClientInterface):
        def evaluate_answer(self, question_front: str, correct_back: str, user_answer: str) -> bool:
            logger.info(f"Mock AI evaluating: Q='{question_front}', Correct='{correct_back}', User='{user_answer}'")
            # Simulate incorrect for Q1 (to test level 0 logic), correct for Q2, Q3
            if "Q1" in question_front and user_answer == "incorrect": # Only first time Q1 is incorrect
                return False
            return True # Simulate correct answer otherwise

    class MockTerminalUI(TerminalUI):
        def __init__(self):
            super().__init__()
            # Simulate user inputs for the test flow
            # Q1 (incorrect, goes to level 0): user types "incorrect", then presses any key for pause
            # Q2 (correct): user types "correct", then presses any key for pause
            # Q3 (correct): user types "correct", then presses any key for pause
            # Q1 (re-appears): user types "correct", then presses any key for pause
            simulated_input_sequence = [
                "incorrect", # User answer for Q1
                "any_key_1", # User presses key after "ŹLE" and correct answer
                "correct",   # User answer for Q2
                "any_key_2", # User presses key after "DOBRZE" and correct answer
                "correct",   # User answer for Q3
                "any_key_3", # User presses key after "DOBRZE" and correct answer
                "correct",   # User answer for re-appeared Q1
                "any_key_4"  # User presses key after "DOBRZE" and correct answer
            ]
            self._inputs = simulated_input_sequence
            self._input_index = 0
            logger.debug("MockTerminalUI initialized.")

        def clear_screen(self) -> None:
            logger.debug("Mock clear screen.")
            print("\n" * 5) # Simulate clearing for test visibility

        def get_user_input(self, prompt: str = "") -> str:
            if self._input_index < len(self._inputs):
                simulated_input = self._inputs[self._input_index]
                # If the current simulated input is meant for wait_for_key_press, consume it
                # and recurse to get the actual user answer.
                if simulated_input.startswith("any_key_"):
                    self._input_index += 1
                    return self.get_user_input(prompt)
                
                self._input_index += 1
                logger.debug(f"Simulating user input: '{simulated_input}'")
                print(f"{prompt}{simulated_input}") # Show what's being "typed"
                return simulated_input
            return TerminalUI.EXIT_KEY # Default to exit if no more inputs

        def wait_for_key_press(self, prompt: str = "Naciśnij dowolny klawisz, aby kontynuować (lub 'q' aby wyjść)...") -> str:
            logger.debug("Mock waiting for key press.")
            print(prompt, end='', flush=True) # Print prompt without newline and flush it
            time.sleep(0.5) # Add a small delay for better test visibility
            if self._input_index < len(self._inputs):
                simulated_input = self._inputs[self._input_index]
                self._input_index += 1
                logger.debug(f"Simulating wait input: '{simulated_input}'")
                print(simulated_input) # Show what's being "typed" or just a newline if empty
                return simulated_input
            print("Simulating Enter.") # Fallback if _inputs exhausted
            return "" # Simulate pressing Enter (empty string)

        def display_message(self, message: str) -> None:
            logger.info(f"Mock Displayed Message: {message}")
            print(f"\n--- MESSAGE ---\n{message}\n---------------\n")

    # --- Assemble and run the Application with mocks ---
    mock_config = MockConfigManager()
    mock_repo = MockFlashcardRepository()
    mock_flashcard_manager = FlashcardManager(mock_repo)
    mock_srs_manager = SRSManager(mock_config)
    mock_ai_client = MockAIClient()
    mock_ui = MockTerminalUI()

    app = Application(
        config_manager=mock_config,
        flashcard_manager=mock_flashcard_manager,
        srs_manager=mock_srs_manager,
        ai_client=mock_ai_client,
        ui=mock_ui
    )

    print("\n--- Running Mock Application Test ---")
    app.run()
    print("--- Mock Application Test Finished ---")

    # Verify state after mock run (optional)
    print("\nFinal state of mock flashcards in repository:")
    for fc in mock_repo._mock_data:
        print(f"  ID: {fc.id.hex[:8]}..., Front: '{fc.front}', Level: {fc.mastery_level}, Last Answer: {fc.last_answer_date}")