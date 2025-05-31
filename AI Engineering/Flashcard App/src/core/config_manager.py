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