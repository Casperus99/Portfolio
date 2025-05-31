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