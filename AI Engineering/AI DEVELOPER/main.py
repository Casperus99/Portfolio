# main.py

import os
import logging
from src.application import Application

# Get a logger for the main script.
logger = logging.getLogger(__name__)

def main() -> None:
    """
    Main entry point for the application.
    Configures user-defined parameters, initializes the Application, and runs it.
    """
    # --- USER CONFIGURATION START ---
    #
    # This section contains parameters that the user can modify to
    # customize the application's behavior.
    #

    # Define the absolute path to the project directory that the AI will analyze and modify.
    # IMPORTANT: Replace "my_test_project" with the actual path to your project.
    # For example: "/home/user/my_awesome_project" or "C:\\Users\\YourUser\\Projects\\MyProject"
    # If the project is in the same directory as main.py, you can use "./my_test_project".
    project_root_path = os.path.abspath("./test_project") # Example path for testing

    # Define the specific instruction or task for the AI model.
    # This prompt will guide the AI in generating code or making modifications.
    user_instruction = "Refactor the 'greet' function in src/main.py to also return the current timestamp."

    # Application-wide configuration settings.
    # - "log_level": Controls the verbosity of logging (e.g., logging.DEBUG, logging.INFO, logging.WARNING).
    # - "gemini_model_name": Specifies which Gemini model to use.
    app_config = {
        "log_level": logging.DEBUG,  # Set to DEBUG for verbose output during development
        "gemini_model_name": "gemini-pro" # Or "gemini-1.5-pro" if you have access and prefer it
    }

    #
    # --- USER CONFIGURATION END ---

    # --- API KEY INSTRUCTION ---
    # The Google API Key for Gemini is loaded from an environment variable for security reasons.
    # Please set it before running the application.
    # For example (Linux/macOS): export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    # For example (Windows CMD): set GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    # For example (Windows PowerShell): $env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    # Alternatively, you can use a .env file and a library like `python-dotenv` for local development.
    # For this project, we assume it's set in the environment.
    # --- END API KEY INSTRUCTION ---


    logger.info("Starting the main application script.")

    # Validate the project path before proceeding.
    if not os.path.isdir(project_root_path):
        logger.critical(f"Project path does not exist: {project_root_path}")
        logger.critical("Please ensure the 'project_root_path' in main.py points to a valid directory.")
        return

    try:
        # Initialize the main Application orchestrator.
        # The GeminiClient initialization within Application will check for GOOGLE_API_KEY.
        app = Application(project_path=project_root_path, config=app_config)
        # Execute the application's main logic with the user's instruction.
        app.run(user_prompt_instruction=user_instruction)
    except ValueError as e:
        # Catch specific ValueError from GeminiClient if API key is missing
        logger.critical(f"Application startup failed due to configuration error: {e}")
    except Exception as e:
        # Catch any other unhandled exceptions during application execution and log them.
        logger.critical(f"An unhandled error occurred during application execution: {e}", exc_info=True)

    logger.info("Main application script finished.")

if __name__ == "__main__":
    main()