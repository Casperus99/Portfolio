# Flashcards SRS Application Documentation

## 1. Introduction

### 1.1. Purpose

The "Flashcards SRS" application is designed to facilitate learning and knowledge retention across various subjects. It employs the Spaced Repetition System (SRS) methodology, an algorithm that optimizes the learning process by adjusting the review frequency of flashcards based on the user's demonstrated mastery.

### 1.2. Core Features

*   **Interactive Quiz:** Presents open-ended questions to the user, with answers evaluated by an AI model.
*   **AI-Powered Feedback:** For incorrect answers, the AI can provide a brief explanation of why the answer was wrong.
*   **Spaced Repetition System (SRS):** Dynamically schedules flashcard reviews based on historical performance and current mastery level.
*   **Progress Tracking:**
    *   Maintains an individual mastery level for each flashcard (configurable, typically 0-6).
    *   Records the date of the last answer for each flashcard.
    *   Displays a summary of overall knowledge distribution by mastery level.
    *   Informs the user of the number of flashcards due for review on the current day.
*   **Flashcard Management:** Stores flashcard data (question, answer, correct answer, mastery level, last answer date, optional evaluation hint) in JSON files.
*   **Data Persistence:** User progress is saved after each answered flashcard.
*   **Simple User Interface:** Operated via keyboard input in a terminal environment.

### 1.3. Technology Stack

*   **Programming Language:** Python 3
*   **AI Integration:** Utilizes an AI model (e.g., Google Gemini) for answer evaluation, with the design allowing for future extensibility to other AI providers.

## 2. Getting Started

### 2.1. Prerequisites

*   Python 3.x installed.
*   Required Python packages (e.g., `google-generativeai` for Gemini integration). These can typically be installed via `pip`.

### 2.2. Project Structure (High-Level)

The application is organized into the following main directories:

*   `main.py`: The main entry point to launch the application.
*   `src/`: Contains all the application's source code modules.
*   `config/`: Holds configuration files, primarily `settings.json`.
*   `flashcards/`: The default directory for storing flashcard data in JSON format. This directory can contain subdirectories representing categories (e.g., "Health"), which in turn contain JSON files for specific decks (e.g., "fruits.json").

### 2.3. Running the Application

The application is launched by executing the `main.py` script from the project's root directory:
```bash
python main.py
```

## 3. User Guide

### 3.1. Main Interface

Upon launching, the terminal interface displays:

*   **Session Statistics:**
    *   `Dostępnych pytań w tym dniu: X` (Available questions today: X)
    *   `Ogólny stan wiedzy (poziomy X-Y): A|B|C|D|E|F|G` (Overall knowledge state (levels X-Y): A|B|C|D|E|F|G) - e.g., `12|43|0|15|1|0|5` indicates 12 cards at level 0, 43 at level 1, etc.
*   **Current Question Context:**
    *   `{Category} - {Deck}, Poziom znajomości: {Mastery Level}` (e.g., Health - Fruits, Mastery Level: 3)
*   **Question Content:**
    *   The text of the question.
*   **Answer Prompt:**
    *   A prompt for the user to type their answer (e.g., `Twoja odpowiedź: `).

### 3.2. Interaction

*   **Answering Questions:** The user types their answer and presses Enter.
*   **Exiting the Application:** The user can press `q` (or `Q`) and then Enter when prompted for an answer, or press `q` when prompted to continue after feedback, to exit the application. Progress is saved upon exit.

### 3.3. Feedback After Answering

*   **Correct Answer:**
    *   The message `^^^   DOBRZE   ^^^` is displayed.
    *   The correct answer is shown:
        ```
        Poprawna odpowiedź:
        {Correct Answer Text}
        ```
    *   The application waits for any key press (or `q` to exit).
*   **Incorrect Answer:**
    *   The message `###   ŹLE   ###` is displayed.
    *   An optional explanation from the AI may be shown:
        ```
        Wyjaśnienie AI:
        {AI-generated explanation text}
        ```
    *   The correct answer is shown:
        ```
        Poprawna odpowiedź:
        {Correct Answer Text}
        ```
    *   The application waits for any key press (or `q` to exit).

### 3.4. Spaced Repetition System (SRS) Logic

Each flashcard has a `mastery_level`. The system uses this level and the `last_answer_date` to determine the next review. Default intervals (configurable) are:

| Mastery Level | Minimum Interval for Next Review |
|---------------|----------------------------------|
| 0             | Same day                         |
| 1             | 1 day                            |
| 2             | 2 days                           |
| 3             | 4 days                           |
| 4             | 7 days                           |
| 5             | 12 days                          |
| 6             | 20 days                          |

*   **Correct Answer:** `mastery_level` increases by 1 (up to the defined maximum).
*   **Incorrect Answer:** `mastery_level` decreases by 1 (down to the minimum, 0).
*   The current date is saved as `last_answer_date`.
*   Flashcards with `mastery_level` 0 are added back to the current session's review queue (not immediately, but later in the same session).

### 3.5. Other Messages

*   **`Gratulacje! Na dziś nie ma więcej pytań do powtórki.`**: (Congratulations! No more questions to review today.) Displayed if all due cards are answered or none were due at the start.
*   **`Koniec pytań w tym dniu (...) Postępy zostały zapisane.`**: (End of questions for today (...) Progress has been saved.) Displayed after completing all available questions in a session.
*   **`Zapisano postępy. Do zobaczenia!`**: (Progress saved. See you!) Displayed when exiting via the 'q' key.

## 4. Data Management

### 4.1. Flashcard Data Format (JSON)

Flashcards are stored in JSON files. Each file contains a list of flashcard objects. A single flashcard object has the following structure:

```json
{
  "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "front": "Question text?",
  "back": "Answer text.",
  "mastery_level": 3,
  "last_answer_date": "2025-03-25",
  "evaluation_hint": "Optional hint for the AI evaluator, e.g., 'Be strict with spelling.'"
}
```

*   **`id`**: A unique UUID for the flashcard. If missing or invalid in the file, a new UUID is generated upon loading.
*   **`front`**: (String) The question content.
*   **`back`**: (String) The correct answer.
*   **`mastery_level`**: (Integer) The current mastery level. Defaults to 0 if missing or invalid.
*   **`last_answer_date`**: (String "YYYY-MM-DD" or `null`) The date of the last review. `null` if never answered.
*   **`evaluation_hint`**: (String, Optional) An optional hint passed to the AI model to guide its evaluation process. If not provided or `null`, it's omitted.

### 4.2. Flashcard Loading

*   The application recursively loads all `.json` files from the directory specified in the configuration (default: `flashcards/`).
*   Subdirectories within the flashcards directory are treated as categories, and JSON filenames (without extension) are treated as deck names.
*   If a JSON file is malformed or contains invalid flashcard data (e.g., missing `front` or `back`), the application will report an error and terminate.

### 4.3. Data Persistence

*   Changes to a flashcard's `mastery_level`, `last_answer_date`, and `evaluation_hint` (if modified programmatically, though typically static) are saved back to its original JSON file after each answer is processed.

## 5. Configuration

Application settings are managed via a `settings.json` file located in the `config/` directory.

```json
{
  "srs_intervals": {
    "0": 0, "1": 1, "2": 2, "3": 4, "4": 7, "5": 12, "6": 20    
  },
  "ai_settings": {
    "api_key": "YOUR_GEMINI_API_KEY",
    "model_name": "gemini-1.5-flash"
  },
  "flashcards_directory": "flashcards/",
  "logging_settings": {
    "log_level": "INFO",
    "log_to_console": false,
    "log_to_file": true,
    "log_file_path": "app.log",
    "clear_log_on_start": true
  }
}
```

*   **`srs_intervals`**: Defines the review interval (in days) for each mastery level.
*   **`ai_settings`**:
    *   `api_key`: The API key for the AI service (e.g., Google Gemini).
    *   `model_name`: The specific AI model to be used.
*   **`flashcards_directory`**: The path to the directory containing flashcard JSON files.
*   **`logging_settings`**:
    *   `log_level`: The minimum logging level (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
    *   `log_to_console`: Boolean; if `true`, logs are output to the console where the application runs.
    *   `log_to_file`: Boolean; if `true`, logs are written to a file.
    *   `log_file_path`: Path to the log file (e.g., "app.log").
    *   `clear_log_on_start`: Boolean; if `true`, the log file is cleared at the beginning of each application session.

## 6. Logging

*   The application uses Python's built-in `logging` module.
*   Log output can be configured to go to the console, a file, or both, as defined in `logging_settings`.
*   The log file can be configured to be cleared at the start of each new session.
*   Log messages include a timestamp, logger name, log level, and the message content.

---
## 7. System Architecture and Design

This section details the internal architecture of the Flashcards SRS application, outlining its layers, classes, and their responsibilities. The design adheres to Object-Oriented Programming (OOP) principles such as the Single Responsibility Principle (SRP), Loose Coupling, and Encapsulation to promote modularity, testability, and extensibility.

### 7.1. Layers Overview

The application is structured into several distinct layers, each with a specific set of responsibilities:

*   **Core Layer (`src/core/`)**: Provides fundamental utilities like configuration management and logging setup.
*   **Data Layer (`src/data/`)**: Manages the flashcard data model, its persistence (loading/saving), and in-memory representation.
*   **SRS Layer (`src/srs/`)**: Implements the Spaced Repetition System algorithm.
*   **AI Integration Layer (`src/ai/`)**: Handles communication with external AI models for answer evaluation.
*   **User Interface Layer (`src/ui/`)**: Manages all interactions with the user via the terminal.
*   **Application Layer (`src/application.py`)**: Orchestrates the interactions between all other layers and manages the main application flow.

### 7.2. Core Layer (`src/core/`)

*   **`logger_setup.py`**:
    *   **Responsibility (SRP):** Configures the application-wide logging system.
    *   **Key Function:** `setup_logging(logging_settings: Dict[str, Any])`
        *   Initializes Python's `logging` module based on settings passed from `ConfigManager`.
        *   Sets up handlers for console and/or file logging.
        *   Handles clearing of the log file if configured.
        *   Sets the logging format and level.
*   **`config_manager.py`**:
    *   **Class:** `ConfigManager`
    *   **Responsibility (SRP):** Loads, validates, and provides access to application settings from `config/settings.json`.
    *   **Key Methods:**
        *   `load_config(file_path: Path)`: Reads and parses the JSON configuration file.
        *   `_validate_config()`: Ensures essential configuration sections and keys are present and have valid types/formats.
        *   `get_setting(key: str, default: Any = None) -> Any`: Retrieves a specific setting.
        *   `get_srs_intervals()`, `get_ai_api_key()`, `get_ai_model_name()`, `get_logging_settings()`: Convenience methods for accessing common configuration groups.
    *   **Interaction:** Used by various components (e.g., `SRSManager`, `GeminiClient`, `Application`, `main.py`) to obtain necessary settings.

### 7.3. Data Layer (`src/data/`)

*   **`flashcard.py`**:
    *   **Class:** `Flashcard` (dataclass)
    *   **Responsibility (SRP):** Represents a single flashcard, encapsulating its attributes (question, answer, mastery level, etc.) and metadata (source file, category, deck, evaluation hint).
    *   **Key Attributes:** `id` (UUID), `front`, `back`, `mastery_level`, `last_answer_date`, `category`, `deck`, `source_file_path`, `evaluation_hint` (Optional[str]).
    *   **Key Methods:**
        *   `from_dict(cls, data: dict, source_file_path: Path, base_flashcards_dir: Path) -> 'Flashcard'`: Factory method to create a `Flashcard` instance from a dictionary (e.g., loaded from JSON), performing validation and deriving category/deck, and loading `evaluation_hint`.
        *   `to_dict() -> dict`: Converts the `Flashcard` instance back to a dictionary suitable for JSON serialization (excluding derived metadata, includes `evaluation_hint` if present).
*   **`flashcard_repository.py`**:
    *   **Class:** `FlashcardRepository`
    *   **Responsibility (SRP):** Handles all file I/O operations for flashcards. It is responsible for reading flashcards from JSON files and writing them back.
    *   **Key Methods:**
        *   `load_flashcards_from_directory(directory_path: Path) -> List[Flashcard]`: Recursively scans the specified directory for `.json` files, parses them, and creates `Flashcard` objects. Handles missing IDs by generating UUIDs and populates `source_file_path`, `category`, `deck`, and `evaluation_hint` for each card.
        *   `save_flashcards(flashcards: List[Flashcard]) -> None`: Saves a list of `Flashcard` objects back to their respective original JSON files. It groups flashcards by `source_file_path` before writing.
    *   **Interaction:** Used by `FlashcardManager` to delegate persistence operations.
*   **`flashcard_manager.py`**:
    *   **Class:** `FlashcardManager`
    *   **Responsibility (SRP):** Manages the collection of `Flashcard` objects in memory during an application session. Acts as an interface to the data for other parts of the application.
    *   **Key Methods:**
        *   `__init__(repository: FlashcardRepository)`: Takes a `FlashcardRepository` instance for dependency injection.
        *   `load_all_flashcards(directory_path: Path)`: Uses the repository to load all flashcards into memory.
        *   `get_all_flashcards() -> List[Flashcard]`: Returns the current list of all managed flashcards.
        *   `get_flashcard_by_id(flashcard_id: UUID) -> Optional[Flashcard]`: Retrieves a specific flashcard.
        *   `update_flashcard(updated_flashcard: Flashcard)`: Updates an existing flashcard in the in-memory collection.
        *   `save_all_flashcards()`: Uses the repository to save all (potentially modified) flashcards.
    *   **Interaction:** Provides flashcard data to `Application` and `SRSManager`.

### 7.4. SRS Layer (`src/srs/`)

*   **`srs_manager.py`**:
    *   **Class:** `SRSManager`
    *   **Responsibility (SRP):** Implements the core logic of the Spaced Repetition System.
    *   **Key Methods:**
        *   `__init__(config_manager: ConfigManager)`: Initializes with SRS intervals from the configuration.
        *   `get_due_flashcards(all_flashcards: List[Flashcard], current_date: date) -> List[Flashcard]`: Filters the list of all flashcards to return only those due for review on the given date.
        *   `update_mastery_level(flashcard: Flashcard, is_correct: bool, current_date: date) -> None`: Modifies the `mastery_level` and `last_answer_date` of a flashcard based on the correctness of the user's answer.
        *   `get_mastery_distribution(all_flashcards: List[Flashcard]) -> Dict[int, int]`: Calculates and returns a dictionary showing how many flashcards exist at each mastery level.
    *   **Interaction:** Used by `Application` to determine which flashcards to present and to update their SRS state.

### 7.5. AI Integration Layer (`src/ai/`)

*   **`evaluation_result.py`**:
    *   **Class:** `EvaluationResult` (dataclass)
    *   **Responsibility (SRP):** Represents the structured result from an AI evaluation, including correctness and an optional explanation.
    *   **Key Attributes:** `is_correct` (bool), `explanation` (Optional[str]).
*   **`ai_client_interface.py`**:
    *   **Class:** `AIClientInterface` (Abstract Base Class)
    *   **Responsibility (SRP):** Defines a common interface for all AI clients. This promotes loose coupling and allows for easy swapping of AI providers.
    *   **Key Abstract Method:**
        *   `evaluate_answer(question_front: str, correct_back: str, user_answer: str, evaluation_hint: Optional[str] = None) -> EvaluationResult`: The contract for evaluating a user's answer, now returning an `EvaluationResult` object.
*   **`gemini_client.py`**:
    *   **Class:** `GeminiClient` (implements `AIClientInterface`)
    *   **Responsibility (SRP):** Handles all communication with the Google Gemini API for answer evaluation.
    *   **Key Methods:**
        *   `__init__(api_key: str, model_name: str)`: Configures the Gemini API client.
        *   `evaluate_answer(question_front: str, correct_back: str, user_answer: str, evaluation_hint: Optional[str] = None) -> EvaluationResult`: Constructs a prompt for the Gemini model (requesting a JSON response with correctness and explanation), sends the request, parses the JSON response, and returns an `EvaluationResult` object.
    *   **Interaction:** Used by `Application` to check the correctness of user answers and get explanations.

### 7.6. User Interface Layer (`src/ui/`)

*   **`terminal_ui.py`**:
    *   **Class:** `TerminalUI`
    *   **Responsibility (SRP):** Manages all input and output operations with the user in the terminal. It is solely responsible for how information is presented and how user input is gathered.
    *   **Key Methods:**
        *   `clear_screen()`: Clears the terminal.
        *   `display_stats(available_count: int, mastery_distribution: Dict[int, int])`: Displays session statistics.
        *   `display_question(flashcard: Flashcard)`: Displays the current flashcard's category, deck, mastery level, and question.
        *   `get_user_input(prompt: str = "") -> str`: Gets multi-character input from the user (for answers).
        *   `display_user_answer(user_answer: str)`: Re-displays the user's entered answer after a screen clear.
        *   `display_correct_answer_feedback()`: Displays "DOBRZE" feedback.
        *   `display_incorrect_feedback_short()`: Displays "ŹLE" feedback.
        *   `display_ai_explanation(explanation: str)`: Displays the AI-generated explanation for an incorrect answer.
        *   `display_correct_answer_only(correct_answer: str)`: Displays the correct answer.
        *   `wait_for_key_press(prompt: str = ...)`: Waits for a single key press without requiring Enter (platform-specific implementation).
        *   `display_message(message: str)`: Displays general messages to the user.
    *   **Interaction:** Used by `Application` to interact with the user.

### 7.7. Application Layer (`src/application.py`)

*   **Class:** `Application`
*   **Responsibility (SRP):** Orchestrates the overall application flow. It initializes and coordinates all other components (layers) to deliver the application's functionality.
*   **Key Methods:**
    *   `__init__(...)`: Constructor that accepts instances of all major components (`ConfigManager`, `FlashcardManager`, `SRSManager`, `AIClientInterface`, `TerminalUI`) via dependency injection.
    *   `run()`: Contains the main application loop. This method:
        1.  Loads flashcards.
        2.  Prepares the current study session by getting due flashcards and shuffling them.
        3.  Enters a loop to present flashcards one by one:
            *   Clears the screen and displays current statistics.
            *   Displays the current flashcard question.
            *   Gets the user's answer.
            *   Handles user exit requests.
            *   Uses the AI client to get an `EvaluationResult` (correctness and optional explanation), passing the `evaluation_hint` from the flashcard.
            *   Updates the flashcard's SRS state based on `EvaluationResult.is_correct`.
            *   Saves progress to disk.
            *   Clears the screen again, displays updated stats, the question, and the user's answer.
            *   Provides feedback: "DOBRZE" or "ŹLE". If "ŹLE" and an AI explanation exists, displays it via `TerminalUI.display_ai_explanation()`. Then shows the correct answer.
            *   Waits for user input to continue.
            *   If an answer was incorrect and the card's level drops to 0, re-adds the card to the end of the current session's queue.
        4.  Displays end-of-session messages.
    *   **Interaction:** Acts as the central coordinator, making calls to methods in all other layers.

### 7.8. Main Entry Point (`main.py`)

*   **Responsibility:** Initializes all the necessary components of the application (ConfigManager, data layer objects, SRSManager, AIClient, TerminalUI) and then creates and runs an instance of the `Application` class.
*   Handles critical startup errors, such as failure to load configuration or initialize the AI client.