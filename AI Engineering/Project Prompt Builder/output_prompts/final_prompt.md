## Project Context Overview ##
Hello Gemini,

You are being provided with a comprehensive overview of a Python project. This context is crucial for any subsequent tasks or questions I might pose regarding the codebase, architecture, or documentation.

Please review the following sections thoroughly:
1.  **Project Directory Structure:** A visual representation of the project's file and folder hierarchy.
2.  **Source Code Section:** The complete source code of all Python files found within the project, each clearly labeled with its relative path.
3.  **Additional Documentation:** A project documentation file (e.g., README.md) has been provided separately for your reference.

I will follow up with specific questions or tasks after you have assimilated this foundational information.

## Project Directory Structure ##

```
Flashcard App/
├── config/
│   └── settings.json
├── flashcards/
│   └── Zdrowie/
│       └── owoce.json
├── src/
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── ai_client_interface.py
│   │   └── gemini_client.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config_manager.py
│   │   └── logger_setup.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── flashcard.py
│   │   ├── flashcard_manager.py
│   │   └── flashcard_repository.py
│   ├── srs/
│   │   ├── __init__.py
│   │   └── srs_manager.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── terminal_ui.py
│   ├── __init__.py
│   └── application.py
├── app.log
├── backlog.txt
├── main.py
├── README.md
└── requirements.md
```

## Source Code Section ##

Relative path: main.py
```python
import logging
import json # For handling potential JSONDecodeError from data layer
from datetime import date
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

# Import the main application orchestrator
from src.application import Application

# Set up a logger for the main script (will be configured by setup_logging)
logger = logging.getLogger(__name__)

def main() -> None:
    """
    Main entry point of the Flashcards SRS application.
    Initializes all necessary components and runs the application.
    """
    # 1. Initialize ConfigManager and load settings FIRST
    # This is done before full logging setup because logging settings are in config.
    config_manager = ConfigManager()
    config_file_path = Path('config/settings.json')
    try:
        config_manager.load_config(config_file_path)
    except (FileNotFoundError, ValueError, IOError) as e:
        # Basic print to console as full logging might not be set up yet
        print(f"Błąd krytyczny: Nie udało się wczytać lub zweryfikować konfiguracji: {e}", file=sys.stderr)
        sys.exit(1) # Exit if configuration is critical

    # 2. Setup Logging using settings from ConfigManager
    # --- MODIFIED START ---
    logging_settings = config_manager.get_logging_settings()
    setup_logging(logging_settings)
    # --- MODIFIED END ---

    logger.info("Application starting...") # Now this log will go to configured handlers

    # 3. Initialize Data Layer components
    flashcard_repository = FlashcardRepository()
    flashcard_manager = FlashcardManager(flashcard_repository)

    # 4. Initialize SRS Logic Layer component
    srs_manager = SRSManager(config_manager)

    # 5. Initialize AI Integration Layer component
    ai_api_key = config_manager.get_ai_api_key()
    ai_model_name = config_manager.get_ai_model_name()
    ai_client: AIClientInterface # Type hint for the interface
    try:
        ai_client = GeminiClient(api_key=ai_api_key, model_name=ai_model_name)
    except (ValueError, RuntimeError) as e:
        logger.critical(f"Failed to initialize AI client (Gemini): {e}. Exiting.")
        print(f"Błąd krytyczny: Nie udało się zainicjować klienta AI: {e}", file=sys.stderr)
        sys.exit(1) # Exit if AI client cannot be initialized

    # 6. Initialize UI Layer component
    ui = TerminalUI()

    # 7. Initialize and run the main Application orchestrator
    try:
        app = Application(
            config_manager=config_manager,
            flashcard_manager=flashcard_manager,
            srs_manager=srs_manager,
            ai_client=ai_client,
            ui=ui
        )
        app.run()
    except Exception as e:
        logger.critical(f"An unhandled error occurred during application runtime: {e}", exc_info=True)
        ui.display_message(f"Wystąpił nieoczekiwany błąd aplikacji: {e}. Sprawdź logi.")
        sys.exit(1)

    logger.info("Application finished gracefully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```
Relative path: src\application.py
```python
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
```
Relative path: src\__init__.py
```python
"""
This is the root package for the Flashcards SRS application.

It contains sub-packages for core utilities, data management,
spaced repetition system logic, AI integration, and user interface.
"""
# No specific configuration or imports needed here.
# This file serves as a package marker and can contain high-level documentation.
```
Relative path: src\ai\ai_client_interface.py
```python
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
```
Relative path: src\ai\gemini_client.py
```python
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
```
Relative path: src\ai\__init__.py
```python
"""
This package contains modules for integrating with Artificial Intelligence models.

Modules:
- ai_client_interface: Defines the abstract interface for AI clients.
- gemini_client: Implements the AI client for Google Gemini API.
"""
# No specific configuration or imports needed here for initial setup.
# This file simply marks the 'ai' directory as a Python package.
```
Relative path: src\core\config_manager.py
```python
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Set up logging for this module
logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Manages application configuration, loading settings from a JSON file.
    Ensures settings are accessible throughout the application.
    """

    def __init__(self) -> None:
        """
        Initializes the ConfigManager.
        Configuration data will be loaded via the load_config method.
        """
        self._config: Dict[str, Any] = {}
        logger.info("ConfigManager initialized.")

    def load_config(self, file_path: Path) -> None:
        """
        Loads configuration settings from the specified JSON file.

        Args:
            file_path (Path): The path to the configuration JSON file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            json.JSONDecodeError: If the configuration file is not valid JSON.
            ValueError: If essential configuration settings are missing or invalid.
        """
        if not file_path.is_file():
            logger.error(f"Configuration file not found: {file_path}")
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            logger.info(f"Configuration loaded successfully from '{file_path}'.")
            self._validate_config() # Validate after loading
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from config file '{file_path}': {e}")
            raise json.JSONDecodeError(f"Malformed config file: {file_path}. Error: {e}", e.doc, e.pos) from e
        except IOError as e:
            logger.error(f"Error reading config file '{file_path}': {e}")
            raise IOError(f"Could not read config file: {file_path}. Error: {e}") from e
        except Exception as e:
            logger.critical(f"An unexpected error occurred during config loading from '{file_path}': {e}")
            raise

    def _validate_config(self) -> None:
        """
        Validates the loaded configuration to ensure essential settings are present and valid.
        Raises ValueError if validation fails.
        """
        # Validate SRS intervals
        srs_intervals = self.get_setting('srs_intervals')
        if not isinstance(srs_intervals, dict) or not srs_intervals:
            raise ValueError("Configuration 'srs_intervals' is missing or not a valid dictionary.")
        # Ensure all values are integers and non-negative
        for level, interval in srs_intervals.items():
            try:
                if not isinstance(level, str) or not level.isdigit():
                    raise ValueError(f"SRS interval level '{level}' is not a valid integer string.")
                if not isinstance(interval, int) or interval < 0:
                    raise ValueError(f"SRS interval for level {level} is not a valid non-negative integer.")
            except ValueError as e:
                raise ValueError(f"Invalid SRS interval configuration: {e}") from e
        # Convert keys to int for easier access later
        self._config['srs_intervals'] = {int(k): v for k, v in srs_intervals.items()}

        # Validate AI settings
        ai_settings = self.get_setting('ai_settings')
        if not isinstance(ai_settings, dict):
            raise ValueError("Configuration 'ai_settings' is missing or not a valid dictionary.")

        required_ai_keys = ['api_key', 'model_name']
        for key in required_ai_keys:
            if key not in ai_settings or not isinstance(ai_settings[key], str) or not ai_settings[key]:
                raise ValueError(f"AI setting '{key}' is missing or invalid.")

        # --- MODIFIED START ---
        # Validate Logging settings
        logging_settings = self.get_setting('logging_settings')
        if not isinstance(logging_settings, dict):
            raise ValueError("Configuration 'logging_settings' is missing or not a valid dictionary.")

        required_logging_keys = ['log_level', 'log_to_console', 'log_to_file', 'log_file_path', 'clear_log_on_start']
        for key in required_logging_keys:
            if key not in logging_settings:
                raise ValueError(f"Logging setting '{key}' is missing.")

        if not isinstance(logging_settings['log_level'], str) or logging_settings['log_level'].upper() not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            raise ValueError("Logging setting 'log_level' is invalid. Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL.")
        if not isinstance(logging_settings['log_to_console'], bool):
            raise ValueError("Logging setting 'log_to_console' must be a boolean.")
        if not isinstance(logging_settings['log_to_file'], bool):
            raise ValueError("Logging setting 'log_to_file' must be a boolean.")
        if not isinstance(logging_settings['log_file_path'], str) or not logging_settings['log_file_path']:
            raise ValueError("Logging setting 'log_file_path' is missing or not a valid string.")
        if not isinstance(logging_settings['clear_log_on_start'], bool):
            raise ValueError("Logging setting 'clear_log_on_start' must be a boolean.")
        # --- MODIFIED END ---

        logger.info("Configuration validated successfully.")

    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration setting by its key.

        Args:
            key (str): The key of the setting to retrieve.
            default (Any, optional): The default value to return if the key is not found.
                                     Defaults to None.

        Returns:
            Any: The value of the setting, or the default value if not found.
        """
        value = self._config.get(key, default)
        if value is None and default is None:
            logger.debug(f"Attempted to retrieve setting '{key}' which is not found and no default provided.")
        else:
            logger.debug(f"Retrieved setting '{key}': {value}")
        return value

    def get_srs_intervals(self) -> Dict[int, int]:
        """
        Convenience method to get SRS intervals directly, ensuring they are integers.
        """
        return self.get_setting('srs_intervals', {})

    def get_ai_api_key(self) -> str:
        """
        Convenience method to get the AI API key.
        """
        return self.get_setting('ai_settings', {}).get('api_key', '')

    def get_ai_model_name(self) -> str:
        """
        Convenience method to get the AI model name.
        """
        return self.get_setting('ai_settings', {}).get('model_name', '')

    # --- MODIFIED START ---
    def get_logging_settings(self) -> Dict[str, Any]:
        """
        Convenience method to get all logging-related settings.
        """
        return self.get_setting('logging_settings', {})
    # --- MODIFIED END ---

# Example usage (for testing, will be called from main.py)
if __name__ == '__main__':
    from src.core.logger_setup import setup_logging as setup_logging_for_test # Avoid name clash
    setup_logging_for_test({'log_level': 'DEBUG', 'log_to_console': True, 'log_to_file': False, 'log_file_path': '', 'clear_log_on_start': False})

    # Create a dummy config file for testing
    test_config_path = Path('test_config.json')
    dummy_config_content = {
        "srs_intervals": {
            "0": 0, "1": 1, "2": 2, "3": 4, "4": 7, "5": 12, "6": 20
        },
        "ai_settings": {
            "api_key": "YOUR_GEMINI_API_KEY",
            "model_name": "gemini-1.5-flash"
        },
        "flashcards_directory": "flashcards/",
        "logging_settings": { # Added for testing
            "log_level": "DEBUG",
            "log_to_console": True,
            "log_to_file": True,
            "log_file_path": "test_app.log",
            "clear_log_on_start": True
        }
    }
    with open(test_config_path, 'w', encoding='utf-8') as f:
        json.dump(dummy_config_content, f, indent=2)

    config_manager = ConfigManager()
    try:
        config_manager.load_config(test_config_path)
        print(f"SRS Intervals: {config_manager.get_srs_intervals()}")
        print(f"AI API Key: {config_manager.get_ai_api_key()}")
        print(f"AI Model Name: {config_manager.get_ai_model_name()}")
        print(f"Flashcards Dir: {config_manager.get_setting('flashcards_directory')}")
        print(f"Logging Settings: {config_manager.get_logging_settings()}")

        # Test missing setting
        print(f"Non-existent setting: {config_manager.get_setting('non_existent', 'default_value')}")

        # Test invalid config (e.g., missing AI key)
        invalid_config_content = {
            "srs_intervals": {"0": 0},
            "ai_settings": {"model_name": "gemini-1.5-flash"}, # Missing API key
            "logging_settings": {"log_level": "INFO", "log_to_console": True, "log_to_file": False, "log_file_path": "log.log", "clear_log_on_start": False}
        }
        invalid_config_path = Path('invalid_test_config.json')
        with open(invalid_config_path, 'w', encoding='utf-8') as f:
            json.dump(invalid_config_content, f, indent=2)

        print("\nTesting invalid configuration (missing AI key):")
        invalid_config_manager = ConfigManager()
        try:
            invalid_config_manager.load_config(invalid_config_path)
        except ValueError as e:
            print(f"Caught expected error: {e}")

        # Test invalid logging config
        invalid_logging_config_content = {
            "srs_intervals": {"0": 0},
            "ai_settings": {"api_key": "dummy", "model_name": "dummy"},
            "logging_settings": {"log_level": "INVALID", "log_to_console": True, "log_to_file": True, "log_file_path": "log.log", "clear_log_on_start": False}
        }
        invalid_logging_config_path = Path('invalid_logging_test_config.json')
        with open(invalid_logging_config_path, 'w', encoding='utf-8') as f:
            json.dump(invalid_logging_config_content, f, indent=2)

        print("\nTesting invalid logging configuration (invalid log_level):")
        invalid_logging_config_manager = ConfigManager()
        try:
            invalid_logging_config_manager.load_config(invalid_logging_config_path)
        except ValueError as e:
            print(f"Caught expected error: {e}")


    except Exception as e:
        print(f"An error occurred during config manager test: {e}")
    finally:
        # Clean up dummy config files
        if test_config_path.exists():
            test_config_path.unlink()
        if invalid_config_path.exists():
            invalid_config_path.unlink()
        if invalid_logging_config_path.exists():
            invalid_logging_config_path.unlink()
        if Path("test_app.log").exists(): # Clean up test log file
            Path("test_app.log").unlink()
```
Relative path: src\core\logger_setup.py
```python
import logging
import os
from pathlib import Path
from typing import Dict, Any

def setup_logging(logging_settings: Dict[str, Any]) -> None:
    """
    Configures the application's logging system based on provided settings.

    Logs can be directed to the console and/or a file.
    The log file can be cleared at the start of each session.

    Args:
        logging_settings (Dict[str, Any]): A dictionary containing logging configuration,
                                           e.g., 'log_level', 'log_to_console', 'log_to_file',
                                           'log_file_path', 'clear_log_on_start'.
    """
    # Ensure the root logger is reset before reconfiguring,
    # especially important in test environments or if called multiple times.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
        handler.close()

    # Define the logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(log_format)

    # Get log level from settings, default to INFO if not found or invalid
    log_level_str = logging_settings.get('log_level', 'INFO').upper()
    numeric_log_level = getattr(logging, log_level_str, logging.INFO)
    if not isinstance(numeric_log_level, int):
        # Fallback if log_level is invalid, should be caught by ConfigManager validation
        numeric_log_level = logging.INFO
        logging.warning(f"Invalid log level '{log_level_str}' specified in settings. Defaulting to INFO.")

    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(numeric_log_level)

    # Add console handler if enabled
    if logging_settings.get('log_to_console', True):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Add file handler if enabled
    if logging_settings.get('log_to_file', False):
        log_file_path_str = logging_settings.get('log_file_path', 'app.log')
        log_file_path = Path(log_file_path_str)

        # --- MODIFIED START ---
        # Clear log file if requested at the start of the session
        if logging_settings.get('clear_log_on_start', False):
            try:
                # Ensure directory exists
                log_file_path.parent.mkdir(parents=True, exist_ok=True)
                # Open in 'w' mode to truncate (clear) the file
                with open(log_file_path, 'w', encoding='utf-8') as f:
                    f.truncate(0)
                # We log this using a temporary logger to ensure it's not affected by potential issues
                # with the main logger being reconfigured.
                temp_logger = logging.getLogger("logger_setup_temp")
                temp_logger.setLevel(logging.INFO)
                temp_handler = logging.StreamHandler()
                temp_handler.setFormatter(formatter)
                temp_logger.addHandler(temp_handler)
                temp_logger.info(f"Log file '{log_file_path}' cleared at start of session.")
                temp_logger.removeHandler(temp_handler) # Clean up temp handler
                temp_handler.close()
            except IOError as e:
                # Log to console if file clearing fails
                logging.error(f"Failed to clear log file '{log_file_path}': {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred while clearing log file '{log_file_path}': {e}")
        # --- MODIFIED END ---

        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Suppress verbose logging from external libraries
    logging.getLogger('google.generativeai').setLevel(logging.WARNING) # More specific than google.api_core
    logging.getLogger('google.api_core').setLevel(logging.WARNING)
    logging.getLogger('google.auth').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    # Log that logging system is initialized (this will go to configured handlers)
    logging.info(f"Logging system initialized with level: {log_level_str}.")

# Example usage (for testing, will be called from main.py)
if __name__ == '__main__':
    test_log_file = Path('test_app_example.log')
    if test_log_file.exists():
        test_log_file.unlink() # Ensure clean slate for testing

    print("--- Testing Console Logging ---")
    setup_logging({
        'log_level': 'DEBUG',
        'log_to_console': True,
        'log_to_file': False,
        'log_file_path': '',
        'clear_log_on_start': False
    })
    logger_test = logging.getLogger(__name__)
    logger_test.debug("This is a debug message to console.")
    logger_test.info("This is an info message to console.")

    print("\n--- Testing File Logging with Clear on Start ---")
    setup_logging({
        'log_level': 'INFO',
        'log_to_console': True, # Still log to console for visibility
        'log_to_file': True,
        'log_file_path': str(test_log_file),
        'clear_log_on_start': True
    })
    logger_test.info("This message should be in the file and console after clear.")
    logger_test.warning("Another warning message.")

    print("\nCheck 'test_app_example.log' file for logs.")

    # Simulate a second run to check clearing
    print("\n--- Simulating Second Run (should clear file again) ---")
    setup_logging({
        'log_level': 'INFO',
        'log_to_console': True,
        'log_to_file': True,
        'log_file_path': str(test_log_file),
        'clear_log_on_start': True
    })
    logger_test.info("This is a message from the second simulated run.")

    print("\nFinal check: 'test_app_example.log' should only contain logs from the second run.")

    if test_log_file.exists():
        test_log_file.unlink()
```
Relative path: src\core\__init__.py
```python
"""
This package contains core utilities for the application,
including configuration management and logging setup.

Modules:
- config_manager: Handles loading and accessing application settings.
- logger_setup: Configures the application's logging system.
"""
# No specific configuration or imports needed here for initial setup.
# This file simply marks the 'core' directory as a Python package.
```
Relative path: src\data\flashcard.py
```python
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
```
Relative path: src\data\flashcard_manager.py
```python
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
```
Relative path: src\data\flashcard_repository.py
```python
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
```
Relative path: src\data\__init__.py
```python
"""
This package contains modules for managing flashcard data.

Modules:
- flashcard: Defines the Flashcard dataclass.
- flashcard_repository: Handles loading and saving flashcards from/to JSON files.
- flashcard_manager: Manages the collection of flashcards in memory.
"""
# No specific configuration or imports needed here for initial setup.
# This file simply marks the 'data' directory as a Python package.
```
Relative path: src\srs\srs_manager.py
```python
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
```
Relative path: src\srs\__init__.py
```python
"""
This package contains modules related to the Spaced Repetition System (SRS) logic.

Modules:
- srs_manager: Implements the core SRS algorithm for determining flashcard due dates
               and updating mastery levels.
"""
# No specific configuration or imports needed here for initial setup.
# This file simply marks the 'srs' directory as a Python package.
```
Relative path: src\ui\terminal_ui.py
```python
import logging
import os
import sys
from typing import Dict
from src.data.flashcard import Flashcard

# Platform-specific imports for single character input
if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix-like (Linux, macOS)
    import termios
    import tty

# Set up logging for this module
logger = logging.getLogger(__name__)

class TerminalUI:
    """
    Handles all user interface interactions in the terminal.
    Responsible for displaying information, prompts, and collecting user input.
    """

    # Define the special exit key
    EXIT_KEY = 'q'

    def __init__(self) -> None:
        """
        Initializes the TerminalUI.
        """
        logger.info("TerminalUI initialized.")

    def clear_screen(self) -> None:
        """
        Clears the terminal screen.
        Works for both Windows ('cls') and Unix/macOS ('clear') systems.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.debug("Terminal screen cleared.")

    def display_stats(self, available_count: int, mastery_distribution: Dict[int, int]) -> None:
        """
        Displays the session statistics to the user.

        Args:
            available_count (int): Number of questions available for review today.
            mastery_distribution (Dict[int, int]): Dictionary showing the count of flashcards
                                                   at each mastery level.
        """
        mastery_levels_str = "|".join(str(mastery_distribution.get(level, 0))
                                      for level in sorted(mastery_distribution.keys()))
        min_level = min(mastery_distribution.keys()) if mastery_distribution else 0
        max_level = max(mastery_distribution.keys()) if mastery_distribution else 6

        print("-" * 50)
        print(f"Dostępnych pytań w tym dniu: {available_count}")
        print(f"Ogólny stan wiedzy (poziomy {min_level}-{max_level}): {mastery_levels_str}")
        print("-" * 50)
        logger.debug(f"Displayed stats: Available={available_count}, Distribution={mastery_distribution}")

    def display_question(self, flashcard: Flashcard) -> None:
        """
        Displays the current flashcard's question to the user.

        Args:
            flashcard (Flashcard): The Flashcard object to display.
        """
        print(f"{flashcard.category} - {flashcard.deck}, Poziom znajomości: {flashcard.mastery_level}")
        print() # Empty line after category/deck/level
        print(f"{flashcard.front}") # Removed "Pytanie:" prefix
        print() # Empty line after question
        logger.info(f"Displayed question for Flashcard ID: {flashcard.id}")

    def get_user_input(self, prompt: str = "") -> str:
        """
        Prompts the user for input and returns their response.
        Handles the special exit key. This method is for multi-character input
        and requires Enter to confirm.

        Args:
            prompt (str): The prompt message to display to the user.

        Returns:
            str: The user's input. If the exit key is pressed, returns the exit key.
        """
        try:
            user_input = input(prompt).strip()
            if user_input.lower() == self.EXIT_KEY:
                logger.info(f"User entered exit key '{self.EXIT_KEY}'.")
            logger.debug(f"User input received (first 20 chars): '{user_input[:20]}'")
            return user_input
        except EOFError:
            logger.warning("EOFError encountered. Assuming exit.")
            return self.EXIT_KEY
        except KeyboardInterrupt:
            logger.warning("KeyboardInterrupt detected. Assuming exit.")
            return self.EXIT_KEY
        except Exception as e:
            logger.error(f"An unexpected error occurred while getting user input: {e}")
            return self.EXIT_KEY # Fallback to exit

    # --- MODIFIED START ---
    def display_user_answer(self, user_answer: str) -> None:
        """
        Displays the user's previously entered answer.
        This is used to re-display the answer after screen clear for feedback.
        """
        print(f"Twoja odpowiedź: {user_answer}")
        logger.debug(f"Re-displayed user answer: '{user_answer}'")
    # --- MODIFIED END ---

    def display_correct_answer_feedback(self) -> None:
        """
        Displays feedback for a correct answer in the specified format.
        """
        print("\n^^^   DOBRZE   ^^^") # Changed to new format
        logger.info("Displayed correct answer feedback.")

    def display_incorrect_feedback_short(self) -> None:
        """
        Displays a short feedback for an incorrect answer.
        """
        print("\n###   ŹLE   ###")
        logger.info("Displayed short incorrect answer feedback.")

    def display_correct_answer_only(self, correct_answer: str) -> None:
        """
        Displays only the correct answer.
        """
        print("\nPoprawna odpowiedź:")
        print(f"{correct_answer}")
        logger.info(f"Displayed correct answer: '{correct_answer}'")

    def wait_for_key_press(self, prompt: str = "Naciśnij dowolny klawisz, aby kontynuować (lub 'q' aby wyjść)...") -> str:
        """
        Waits for the user to press any key without requiring Enter.
        This uses platform-specific methods for non-buffered input.

        Args:
            prompt (str): The message to display while waiting.

        Returns:
            str: The key pressed by the user. Returns EXIT_KEY if the user
                 enters the exit key or an interrupt occurs.
        """
        print(prompt, end='', flush=True) # Print prompt without newline and flush it

        key_pressed = ''
        try:
            if os.name == 'nt': # Windows
                key_pressed_bytes = msvcrt.getch()
                key_pressed = key_pressed_bytes.decode('utf-8') # Decode bytes to string
            else: # Unix-like
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd) # Set terminal to raw mode
                    key_pressed = sys.stdin.read(1) # Read a single character
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) # Restore terminal settings

            # Print the pressed key for feedback, then a newline
            print(key_pressed)
            
            if key_pressed.lower() == self.EXIT_KEY:
                logger.debug(f"User pressed exit key '{self.EXIT_KEY}' during wait.")
            return key_pressed
        except (EOFError, KeyboardInterrupt):
            logger.warning("Interrupt detected during key press wait. Exiting.")
            return self.EXIT_KEY
        except Exception as e:
            logger.error(f"An unexpected error occurred while waiting for key press: {e}")
            return self.EXIT_KEY

    def display_message(self, message: str) -> None:
        """
        Displays a general message to the user.

        Args:
            message (str): The message string to display.
        """
        print(f"\n{message}\n")
        logger.info(f"Displayed message: '{message}'")

# Example usage (for testing, will be called from main.py)
if __name__ == '__main__':
    from src.core.logger_setup import setup_logging
    from datetime import date
    from uuid import uuid4
    from pathlib import Path
    import time # For test delays

    # Configure logging for the test block (independent of app's config)
    setup_logging({
        'log_level': 'DEBUG',
        'log_to_console': True,
        'log_to_file': False,
        'log_file_path': 'test_ui.log',
        'clear_log_on_start': True
    })
    ui = TerminalUI()

    # Test clear_screen (might flash quickly)
    print("Clearing screen in 2 seconds...")
    time.sleep(2)
    ui.clear_screen()
    print("Screen cleared.")

    # Test display_stats
    print("\n--- Testing display_stats ---")
    mock_mastery_distribution = {0: 10, 1: 5, 2: 3, 3: 1, 4: 0, 5: 2, 6: 1}
    ui.display_stats(available_count=15, mastery_distribution=mock_mastery_distribution)

    # Test display_question
    print("\n--- Testing display_question ---")
    mock_flashcard = Flashcard(
        front="What is the capital of Poland?",
        back="Warsaw",
        source_file_path=Path("flashcards/Geography/Europe.json"),
        id=uuid4(),
        mastery_level=2,
        last_answer_date=date.today(),
        category="Geography",
        deck="Europe"
    )
    ui.display_question(mock_flashcard)

    # Test get_user_input
    print("\n--- Testing get_user_input (type 'q' to test exit) ---")
    user_answer_test = ui.get_user_input("Twoja odpowiedź: ")
    print(f"User entered: '{user_answer_test}'")
    if user_answer_test.lower() == ui.EXIT_KEY:
        print("User chose to exit.")

    # Test new incorrect feedback flow
    print("\n--- Testing incorrect feedback flow ---")
    user_answer_mock = "Londyn"
    correct_answer_mock = "Warszawa"

    ui.clear_screen() # Simulate clear before re-displaying context
    ui.display_stats(14, {0: 11, 1: 4, 2: 3, 3: 1, 4: 0, 5: 2, 6: 1}) # Updated stats
    ui.display_question(mock_flashcard) # Re-display question
    ui.display_user_answer(user_answer_mock) # Re-display user's answer

    ui.display_incorrect_feedback_short() # First feedback: "###   ŹLE   ###"
    
    print("\n(Simulating wait for key press after 'ŹLE.')")
    _ = ui.wait_for_key_press(prompt="Press any key to show correct answer (mock)...") # Simulate user pressing a key
    
    ui.display_correct_answer_only(correct_answer_mock) # Show correct answer

    print() # Add empty line before the next wait prompt as requested
    print("(Simulating second wait for key press after correct answer)")
    _ = ui.wait_for_key_press(prompt="Press any key to continue mock test...") # Simulate user pressing a key

    # Test correct feedback flow
    print("\n--- Testing correct feedback flow ---")
    user_answer_mock_correct = "Warsaw"
    ui.clear_screen() # Simulate clear before re-displaying context
    ui.display_stats(13, {0: 10, 1: 5, 2: 3, 3: 1, 4: 0, 5: 2, 6: 1}) # Updated stats
    ui.display_question(mock_flashcard) # Re-display question
    ui.display_user_answer(user_answer_mock_correct) # Re-display user's answer

    ui.display_correct_answer_feedback() # Show "^^^ DOBRZE ^^^"
    ui.display_correct_answer_only("Warsaw") # Show correct answer
    
    print() # Add empty line before the next wait prompt
    print("(Simulating wait for key press after 'DOBRZE' and correct answer)")
    _ = ui.wait_for_key_press(prompt="Press any key to continue mock test...")


    # Test display_message
    print("\n--- Testing display_message ---")
    ui.display_message("Gratulacje! Na dziś nie ma więcej pytań do powtórki.")

    print("\nTerminalUI tests finished.")
```
Relative path: src\ui\__init__.py
```python
"""
This package contains modules for the user interface, specifically for terminal interaction.

Modules:
- terminal_ui: Handles displaying information and collecting input in the terminal.
"""
# No specific configuration or imports needed here for initial setup.
# This file simply marks the 'ui' directory as a Python package.
```
