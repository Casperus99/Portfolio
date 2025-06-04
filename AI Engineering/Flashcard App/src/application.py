# Relative path: src/application.py
import logging
import json 
from datetime import date, timedelta 
from pathlib import Path
import random 
import sys 
from typing import List, Optional

from src.core.logger_setup import setup_logging
from src.core.config_manager import ConfigManager
from src.data.flashcard_repository import FlashcardRepository
from src.data.flashcard_manager import FlashcardManager
from src.srs.srs_manager import SRSManager
from src.ai.ai_client_interface import AIClientInterface 
from src.ai.evaluation_result import EvaluationResult # Import new result class
from src.ui.terminal_ui import TerminalUI
from src.data.flashcard import Flashcard 

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
        """
        self._config_manager = config_manager
        self._flashcard_manager = flashcard_manager
        self._srs_manager = srs_manager
        self._ai_client = ai_client
        self._ui = ui
        self._running = True 
        logger.info("Application initialized.")

    def run(self) -> None:
        """
        Starts the main application loop.
        Handles loading data, running the quiz session, and saving progress.
        """
        logger.info("Application started.")
        self._ui.clear_screen()

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

        current_date_val = date.today()
        due_flashcards_for_session = self._srs_manager.get_due_flashcards(all_flashcards, current_date_val)
        random.shuffle(due_flashcards_for_session) 

        if not due_flashcards_for_session:
            self._ui.display_message("Gratulacje! Na dziś nie ma więcej pytań do powtórki.")
            logger.info("No flashcards due for review today. Exiting.")
            return

        logger.info(f"Starting quiz session with {len(due_flashcards_for_session)} initially due flashcards.")

        while self._running and due_flashcards_for_session:
            self._ui.clear_screen()
            mastery_dist = self._srs_manager.get_mastery_distribution(all_flashcards)
            self._ui.display_stats(len(due_flashcards_for_session), mastery_dist)

            current_flashcard: Flashcard = due_flashcards_for_session[0] 

            self._ui.display_question(current_flashcard)
            user_answer = self._ui.get_user_input("Twoja odpowiedź: ")

            if user_answer.lower() == self._ui.EXIT_KEY: 
                self._running = False
                logger.info("User requested exit during input.")
                break 

            logger.debug(f"Evaluating answer for flashcard ID: {current_flashcard.id} with hint: '{current_flashcard.evaluation_hint}'")
            evaluation_result: EvaluationResult = self._ai_client.evaluate_answer(
                question_front=current_flashcard.front,
                correct_back=current_flashcard.back,
                user_answer=user_answer,
                evaluation_hint=current_flashcard.evaluation_hint 
            )
            is_correct = evaluation_result.is_correct # Extract boolean for SRS logic

            self._srs_manager.update_mastery_level(current_flashcard, is_correct, current_date_val)
            self._flashcard_manager.update_flashcard(current_flashcard)

            try:
                self._flashcard_manager.save_all_flashcards()
                logger.info(f"Progress saved for flashcard ID: {current_flashcard.id}")
            except (IOError, Exception) as e:
                logger.error(f"Failed to save flashcard progress for ID {current_flashcard.id}: {e}")
                self._ui.display_message(f"Błąd zapisu postępów dla fiszki {current_flashcard.id}: {e}")

            self._ui.clear_screen()
            mastery_dist = self._srs_manager.get_mastery_distribution(all_flashcards) 
            
            temp_available_count = len(due_flashcards_for_session)
            if is_correct:
                if temp_available_count > 0:
                    temp_available_count -=1
            else: 
                if current_flashcard.mastery_level != self._srs_manager._min_mastery_level:
                    if temp_available_count > 0:
                        temp_available_count -=1
            self._ui.display_stats(temp_available_count if temp_available_count >=0 else 0, mastery_dist)
            
            self._ui.display_question(current_flashcard) 
            self._ui.display_user_answer(user_answer) 

            if is_correct:
                self._ui.display_correct_answer_feedback() 
                self._ui.display_correct_answer_only(current_flashcard.back) 
                print() 
                
                wait_input = self._ui.wait_for_key_press()
                if wait_input.lower() == self._ui.EXIT_KEY: 
                    self._running = False
                    logger.info("User requested exit after correct answer.")
                    break 
                
                due_flashcards_for_session.pop(0) 

            else: # Incorrect answer
                self._ui.display_incorrect_feedback_short() 
                if evaluation_result.explanation: # Display AI explanation if available
                    self._ui.display_ai_explanation(evaluation_result.explanation)
                self._ui.display_correct_answer_only(current_flashcard.back) 
                print() 
                
                wait_input = self._ui.wait_for_key_press()
                if wait_input.lower() == self._ui.EXIT_KEY: 
                    self._running = False
                    logger.info("User requested exit after incorrect answer.")
                    break 

                if current_flashcard.mastery_level == self._srs_manager._min_mastery_level:
                    card_to_readd = due_flashcards_for_session.pop(0) 
                    due_flashcards_for_session.append(card_to_readd) 
                    logger.debug(f"Flashcard ID {current_flashcard.id} moved to end of due list (level {current_flashcard.mastery_level}).")
                else:
                    due_flashcards_for_session.pop(0) 

        self._ui.clear_screen()
        if not self._running:
            self._ui.display_message("Zapisano postępy. Do zobaczenia!")
            logger.info("Application exited by user request.")
        else:
            self._ui.display_message("Koniec pytań w tym dniu. Postępy zostały zapisane.")
            logger.info("All due flashcards for today have been reviewed. Session ended.")

        logger.info("Application finished gracefully.")

if __name__ == '__main__':
    from src.core.logger_setup import setup_logging
    from src.core.config_manager import ConfigManager
    from src.data.flashcard import Flashcard
    from src.data.flashcard_repository import FlashcardRepository
    from src.ai.ai_client_interface import AIClientInterface
    from src.ai.evaluation_result import EvaluationResult # Import for mock
    from src.ui.terminal_ui import TerminalUI
    from uuid import uuid4
    import os
    import time 

    try:
        setup_logging({
            'log_level': 'DEBUG',
            'log_to_console': True, 
            'log_to_file': False,
            'log_file_path': 'test_app.log',
            'clear_log_on_start': True
        })
    except TypeError: 
        setup_logging('DEBUG')

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
                Flashcard(front="Mock Q1 (lvl0, hint)", back="Mock A1", mastery_level=0, last_answer_date=None, category="mock", deck="test", source_file_path=Path("mock_flashcards/mock/test.json"), evaluation_hint="Be strict with Q1"),
                Flashcard(front="Mock Q2 (lvl1 due)", back="Mock A2", mastery_level=1, last_answer_date=date.today() - timedelta(days=1), category="mock", deck="test", source_file_path=Path("mock_flashcards/mock/test.json")),
                Flashcard(front="Mock Q3 (lvl2 due, fruit example)", back="jabłko, banan", mastery_level=2, last_answer_date=date.today() - timedelta(days=2), category="mock", deck="test", source_file_path=Path("mock_flashcards/mock/test.json"), evaluation_hint="Check for listed fruits."),
            ]
            logger.debug("MockFlashcardRepository initialized.")

        def load_flashcards_from_directory(self, directory_path: Path) -> List[Flashcard]:
            logger.info(f"Mock loading flashcards from {directory_path}. Returning {len(self._mock_data)} mock cards.")
            return list(self._mock_data) 

        def save_flashcards(self, flashcards: List[Flashcard]) -> None:
            logger.info(f"Mock saving {len(flashcards)} flashcards.")
            for fc_to_save in flashcards:
                found = False
                for i, mock_fc in enumerate(self._mock_data):
                    if mock_fc.id == fc_to_save.id:
                        self._mock_data[i] = fc_to_save 
                        found = True
                        break
                if not found: 
                     self._mock_data.append(fc_to_save)
            logger.debug("Mock flashcards updated in repository.")

    class MockAIClient(AIClientInterface):
        def evaluate_answer(self, question_front: str, correct_back: str, user_answer: str, evaluation_hint: Optional[str] = None) -> EvaluationResult:
            logger.info(f"Mock AI evaluating: Q='{question_front}', Correct='{correct_back}', User='{user_answer}', Hint='{evaluation_hint}'")
            
            if "Q1" in question_front and evaluation_hint == "Be strict with Q1":
                if user_answer == "incorrect_q1": 
                    return EvaluationResult(is_correct=False, explanation="Mock explanation for Q1: Answer 'incorrect_q1' is wrong based on strict hint.")
                if user_answer == correct_back:
                    return EvaluationResult(is_correct=True)
                return EvaluationResult(is_correct=False, explanation="Mock explanation for Q1: Strict check failed.")

            if "Q3" in question_front: # Fruit example
                if user_answer == "jabłko, kiwi":
                    return EvaluationResult(is_correct=False, explanation="Mock explanation for Q3: Podałeś 'kiwi', które jest błędne, i nie podałeś 'banana'.")
                if user_answer == correct_back: # "jabłko, banan"
                    return EvaluationResult(is_correct=True)
            
            # Default behavior
            if "correct" in user_answer.lower() or user_answer.lower() == correct_back.lower():
                return EvaluationResult(is_correct=True)
            
            return EvaluationResult(is_correct=False, explanation="Mock general explanation: Your answer was not deemed correct.")

    class MockTerminalUI(TerminalUI):
        def __init__(self):
            super().__init__()
            # Q1 (strict hint, user types "incorrect_q1"): Incorrect -> Lvl 0, with explanation
            # Q2 (no hint, user types "correct"): Correct -> Lvl 2
            # Q3 (fruit example, user types "jabłko, kiwi"): Incorrect -> Lvl 1, with explanation
            # Q1 (re-appears, strict hint, user types "Mock A1"): Correct -> Lvl 1
            simulated_input_sequence = [
                "incorrect_q1", # User answer for Q1
                "any_key_1",    # Pause
                "correct",      # User answer for Q2
                "any_key_2",    # Pause
                "jabłko, kiwi", # User answer for Q3
                "any_key_3",    # Pause
                "Mock A1",      # User answer for re-appeared Q1
                "any_key_4"     # Pause
            ]
            self._inputs = simulated_input_sequence
            self._input_index = 0
            logger.debug("MockTerminalUI initialized.")

        def clear_screen(self) -> None:
            logger.debug("Mock clear screen.")
            print("\n" * 1) 

        def get_user_input(self, prompt: str = "") -> str:
            if self._input_index < len(self._inputs):
                simulated_input = self._inputs[self._input_index]
                if simulated_input.startswith("any_key_"): 
                    self._input_index += 1
                    return self.get_user_input(prompt) 
                
                self._input_index += 1
                logger.debug(f"Simulating user input: '{simulated_input}' for prompt '{prompt}'")
                print(f"{prompt}{simulated_input}") 
                return simulated_input
            logger.warning("MockTerminalUI ran out of inputs, returning EXIT_KEY.")
            return TerminalUI.EXIT_KEY 

        def wait_for_key_press(self, prompt: str = "Naciśnij dowolny klawisz, aby kontynuować (lub 'q' aby wyjść)...") -> str:
            logger.debug(f"Mock waiting for key press with prompt: '{prompt}'")
            print(prompt, end='', flush=True)
            time.sleep(0.05) 
            if self._input_index < len(self._inputs):
                simulated_input = self._inputs[self._input_index]
                if not simulated_input.startswith("any_key_"): 
                    logger.warning(f"Mock wait_for_key_press expected 'any_key_', got '{simulated_input}'. Simulating Enter.")
                    print("Simulating Enter.")
                    return "" 

                self._input_index += 1
                logger.debug(f"Simulating wait input: '{simulated_input}'")
                print(simulated_input) 
                return simulated_input
            
            logger.warning("MockTerminalUI ran out of inputs for wait_for_key_press. Simulating Enter.")
            print("Simulating Enter.") 
            return "" 

        def display_message(self, message: str) -> None:
            logger.info(f"Mock Displayed Message: {message}")
            print(f"\n--- MESSAGE ---\n{message}\n---------------\n")
        
        def display_ai_explanation(self, explanation: str) -> None:
            message = f"Wyjaśnienie AI: {explanation}"
            print(f"\n{message}\n")
            logger.info(f"Displayed AI explanation: '{explanation}'")


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

    print("\n--- Running Mock Application Test with AI Explanations ---")
    app.run()
    print("--- Mock Application Test Finished ---")

    print("\nFinal state of mock flashcards in repository:")
    for fc in mock_repo._mock_data: 
        print(f"  ID: {fc.id.hex[:8]}..., Front: '{fc.front}', Level: {fc.mastery_level}, Last Answer: {fc.last_answer_date}, Hint: '{fc.evaluation_hint}'")
    # Expected final states:
    # Q1: Level 1 (incorrect_q1 -> L0, then Mock A1 -> L1)
    # Q2: Level 2 (correct)
    # Q3: Level 1 (jabłko, kiwi -> L1 from L2)