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