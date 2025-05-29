# src/application.py

import logging
from typing import Dict, Any, Optional, Tuple, List
import os

# Import required classes
from src.project_manager import ProjectManager
from src.prompt_formatter import PromptFormatter
from src.gemini_client import GeminiClient # New import
from google.generativeai.types import Part # Still needed for type hints

# Initialize a logger for this module.
logger = logging.getLogger(__name__)

class Application:
    """
    The main orchestrator class for the AI-powered development application.
    It manages the lifecycle of the application, coordinating interactions
    between different components like file loading, AI communication,
    and file updates.
    """

    def __init__(self, project_path: str, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initializes the Application instance.

        Args:
            project_path: The absolute path to the root directory of the project
                          to be processed by the AI.
            config: An optional dictionary for application configuration settings.
                    This can be used for API keys, model names, logging levels, etc.
        """
        self.project_path = project_path
        self.config = config if config is not None else {}

        self._setup_logging()  # Configure logging for the entire application
        logger.info("Application instance initialized.")

        # Initialize ProjectManager instance
        self.project_manager = ProjectManager(self.project_path)

        # Construct the path to the prompts directory
        prompts_directory = os.path.join(self.project_path, "prompts") # Zakładając, że 'prompts' jest w project_path

        # Initialize PromptFormatter instance
        self.prompt_formatter = PromptFormatter()

        # Initialize GeminiClient instance
        # Retrieve model name from config, default to 'gemini-pro' if not specified
        gemini_model_name = self.config.get("gemini_model_name", "gemini-pro")
        try:
            self.gemini_client = GeminiClient(model_name=gemini_model_name)
        except ValueError as e:
            logger.critical(f"Failed to initialize GeminiClient: {e}. Exiting application.")
            # Re-raise the exception or handle it more gracefully depending on application requirements
            raise # Re-raise to stop execution if API key is missing

        # Placeholders for other future component instances.
        self.ai_response_parser = None  # type: Any # Will be AIResponseParser instance
        self.file_updater = None  # type: Any # Will be FileUpdater instance

    def _setup_logging(self) -> None:
        """
        Configures the root logger for the application.
        This method ensures that logging is set up once and consistently
        across all modules that use the `logging` module.
        """
        log_level = self.config.get("log_level", logging.INFO)

        if not logging.getLogger().handlers:
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.StreamHandler()
                ]
            )
        logger.debug(f"Logging configured with level: {logging.getLevelName(log_level)}")


    def run(self, user_prompt_instruction: str) -> None:
        """
        Executes the main application logic.
        This method will orchestrate the steps:
        1. Load project files.
        2. Format context for AI.
        3. Count prompt tokens.
        4. Send request to AI.
        5. Parse AI response.
        6. Update local files.

        Args:
            user_prompt_instruction: The specific instruction from the user
                                     for the AI model (e.g., "Add logging to main.py").
        """
        logger.info(f"Application started with instruction: '{user_prompt_instruction}'")

        # Step 1: Load project files using ProjectManager
        try:
            self.project_manager.load_files()
            logger.info("Project files loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load project files: {e}", exc_info=True)
            return # Exit if file loading fails

        # Step 2: Format context for AI using PromptFormatter
        try:
            python_files = self.project_manager.get_all_python_files()
            docs_md_content = self.project_manager.get_docs_md_content()

            main_prompt_string, gemini_parts = self.prompt_formatter.format_context(
                python_files=python_files,
                docs_md_content=docs_md_content,
                user_instruction=user_prompt_instruction
            )
            if main_prompt_string is None:
                logger.critical("Failed to generate main prompt string because system prompt could not be loaded. Aborting.")
                return
            logger.info("Project context and user instruction formatted for AI.")
        except Exception as e:
            logger.error(f"Failed to format prompt for AI: {e}", exc_info=True)
            return # Exit if prompt formatting fails

        # Step 3: Count prompt tokens using GeminiClient
        try:
            token_count = self.gemini_client.count_prompt_tokens(main_prompt_string, gemini_parts)
            if token_count != -1: # Check if token counting was successful
                logger.info(f"Total tokens for this prompt: {token_count}")
            else:
                logger.warning("Could not retrieve accurate token count.")
        except Exception as e:
            logger.error(f"Error during token counting step: {e}", exc_info=True)
            # Decide if this is a critical error to stop execution or just log and continue.
            # For now, we'll continue, but it's a point for discussion.

        # Step 4: Send request to AI using GeminiClient
        try:
            ai_raw_response = self.gemini_client.send_request(main_prompt_string, gemini_parts)
            if ai_raw_response is None:
                logger.error("AI response was empty or an error occurred during generation.")
                return # Exit if AI response is not received
            logger.info("AI response received successfully.")
            # The raw response will be passed to AIResponseParser in the next step.
        except Exception as e:
            logger.error(f"Failed to get response from AI: {e}", exc_info=True)
            return # Exit if AI communication fails

        # --- Placeholder for remaining application logic ---
        # Step 5: Parse AI response (AIResponseParser)
        # Step 6: Update local files (FileUpdater)

        logger.info("Application finished its execution cycle.")