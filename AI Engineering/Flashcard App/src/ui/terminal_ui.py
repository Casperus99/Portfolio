# Relative path: src/ui/terminal_ui.py
import logging
import os
import sys
from typing import Dict, Optional # Added Optional
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
        min_level_key = min(mastery_distribution.keys()) if mastery_distribution else 0
        max_level_key = max(mastery_distribution.keys()) if mastery_distribution else 6 # Default max level

        print("-" * 50)
        print(f"Dostępnych pytań w tym dniu: {available_count}")
        print(f"Ogólny stan wiedzy (poziomy {min_level_key}-{max_level_key}): {mastery_levels_str}")
        print("-" * 50)
        logger.debug(f"Displayed stats: Available={available_count}, Distribution={mastery_distribution}")

    def display_question(self, flashcard: Flashcard) -> None:
        """
        Displays the current flashcard's question to the user.

        Args:
            flashcard (Flashcard): The Flashcard object to display.
        """
        print(f"{flashcard.category} - {flashcard.deck}, Poziom znajomości: {flashcard.mastery_level}")
        # Display evaluation hint if present, for user awareness or debugging
        # if flashcard.evaluation_hint:
        # print(f"Wskazówka dla AI: {flashcard.evaluation_hint}") # Potentially for debugging, not for user
        print() 
        print(f"{flashcard.front}") 
        print() 
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
            return self.EXIT_KEY 

    def display_user_answer(self, user_answer: str) -> None:
        """
        Displays the user's previously entered answer.
        This is used to re-display the answer after screen clear for feedback.
        """
        print(f"Twoja odpowiedź: {user_answer}")
        logger.debug(f"Re-displayed user answer: '{user_answer}'")

    def display_correct_answer_feedback(self) -> None:
        """
        Displays feedback for a correct answer in the specified format.
        """
        print("\n^^^   DOBRZE   ^^^") 
        logger.info("Displayed correct answer feedback.")

    def display_incorrect_feedback_short(self) -> None:
        """
        Displays a short feedback for an incorrect answer.
        """
        print("\n###   ŹLE   ###")
        logger.info("Displayed short incorrect answer feedback.")

    def display_ai_explanation(self, explanation: str) -> None:
        """
        Displays an explanation provided by the AI for an incorrect answer.

        Args:
            explanation (str): The explanation text from the AI.
        """
        print(f"\nWyjaśnienie AI: {explanation}")
        logger.info(f"Displayed AI explanation: '{explanation}'")

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
        print(prompt, end='', flush=True) 

        key_pressed = ''
        try:
            if os.name == 'nt': 
                key_pressed_bytes = msvcrt.getch()
                try:
                    key_pressed = key_pressed_bytes.decode('utf-8', errors='ignore') 
                except UnicodeDecodeError:
                    key_pressed = key_pressed_bytes.decode('cp1250', errors='ignore') # Common Polish encoding on Windows
                    logger.warning(f"Decoded key press using cp1250 after utf-8 failed: {key_pressed_bytes}")

            else: 
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd) 
                    key_pressed = sys.stdin.read(1) 
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 

            print(key_pressed if key_pressed.isprintable() else '') # Print only printable chars, then newline
            
            if key_pressed.lower() == self.EXIT_KEY:
                logger.debug(f"User pressed exit key '{self.EXIT_KEY}' during wait.")
            return key_pressed
        except (EOFError, KeyboardInterrupt):
            logger.warning("Interrupt detected during key press wait. Exiting.")
            print() # Ensure prompt is not left hanging
            return self.EXIT_KEY
        except Exception as e:
            logger.error(f"An unexpected error occurred while waiting for key press: {e}")
            print() # Ensure prompt is not left hanging
            return self.EXIT_KEY

    def display_message(self, message: str) -> None:
        """
        Displays a general message to the user.

        Args:
            message (str): The message string to display.
        """
        print(f"\n{message}\n")
        logger.info(f"Displayed message: '{message}'")

# Example usage
if __name__ == '__main__':
    from src.core.logger_setup import setup_logging
    from datetime import date
    from uuid import uuid4
    from pathlib import Path
    import time 

    try:
        setup_logging({
            'log_level': 'DEBUG',
            'log_to_console': True,
            'log_to_file': False,
            'log_file_path': 'test_ui.log',
            'clear_log_on_start': True
        })
    except TypeError:
        setup_logging('DEBUG')
        
    ui = TerminalUI()

    print("Clearing screen in 1 seconds...")
    time.sleep(1)
    ui.clear_screen()
    print("Screen cleared.")

    print("\n--- Testing display_stats ---")
    mock_mastery_distribution = {0: 10, 1: 5, 2: 3, 3: 1, 4: 0, 5: 2, 6: 1}
    ui.display_stats(available_count=15, mastery_distribution=mock_mastery_distribution)

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
    print("\n--- Testing display_question ---")
    ui.display_question(mock_flashcard)

    print("\n--- Testing get_user_input (type 'q' to test exit) ---")
    user_answer_test = ui.get_user_input("Twoja odpowiedź: ")
    print(f"User entered: '{user_answer_test}'")
    if user_answer_test.lower() == ui.EXIT_KEY:
        print("User chose to exit.")

    print("\n--- Testing incorrect feedback flow with AI explanation ---")
    user_answer_mock = "Krakow"
    correct_answer_mock = "Warsaw"
    ai_explanation_mock = "Krakow is a major city in Poland, but the capital is Warsaw."

    ui.clear_screen() 
    ui.display_stats(14, {0: 11, 1: 4, 2: 3, 3: 1, 4: 0, 5: 2, 6: 1}) 
    ui.display_question(mock_flashcard) 
    ui.display_user_answer(user_answer_mock) 

    ui.display_incorrect_feedback_short() 
    ui.display_ai_explanation(ai_explanation_mock) # New call
    ui.display_correct_answer_only(correct_answer_mock) 
    print()
    _ = ui.wait_for_key_press(prompt="Press any key to continue mock test...") 

    print("\n--- Testing correct feedback flow ---")
    user_answer_mock_correct = "Warsaw"
    ui.clear_screen() 
    ui.display_stats(13, {0: 10, 1: 5, 2: 3, 3: 1, 4: 0, 5: 2, 6: 1}) 
    ui.display_question(mock_flashcard) 
    ui.display_user_answer(user_answer_mock_correct) 

    ui.display_correct_answer_feedback() 
    ui.display_correct_answer_only("Warsaw") 
    print() 
    _ = ui.wait_for_key_press(prompt="Press any key to continue mock test...")

    print("\n--- Testing display_message ---")
    ui.display_message("Gratulacje! Na dziś nie ma więcej pytań do powtórki.")

    print("\nTerminalUI tests finished.")