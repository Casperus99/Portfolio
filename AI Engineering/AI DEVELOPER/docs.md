# AI-Powered Development Assistant - Project Overview & Design

**Last Updated:** 2025-05-29

## 1. Project Vision & Goal

The primary goal of this project is to develop an innovative application that revolutionizes the developer's interaction with AI models, significantly accelerating the software development process. The vision is for a "software engineer" to focus on conceptualizing functionalities, while the AI, guided by this application, handles their implementation.

Key application functionalities include:
-   Automatically feeding project source materials (code, documentation, tests) to an AI model.
-   Enforcing a templated and predictable response structure from the AI model, specifically a JSON format.
-   Automatically updating local project files based on the AI's structured response.

## 2. Core Architecture

The application employs a modular architecture, promoting flexibility, testability, and scalability. It is being developed in Python.

### 2.1. Key Modules (Python classes in `src/` directory):

*   **`main.py` (Root Directory):**
    *   **Purpose:** Main entry point of the application.
    *   **Responsibilities:** Handles user-configurable parameters (project path, AI instruction, logging level, Gemini model name), initializes the `Application` class, and invokes its `run` method. Contains basic startup error handling.
    *   **Dependencies:** `src.application.Application`.

*   **`src/application.py` -> `Application` class:**
    *   **Purpose:** Acts as the central orchestrator of the application's workflow.
    *   **Responsibilities:**
        *   Initializes and coordinates `ProjectManager`, `PromptFormatter`, and `GeminiClient`.
        *   Manages the application lifecycle in its `run` method:
            1.  Load project files (`ProjectManager`).
            2.  Format project context and user instruction for AI (`PromptFormatter`).
            3.  Count prompt tokens (`GeminiClient`).
            4.  Send request to AI and receive raw response (`GeminiClient`).
            5.  (Planned) Parse AI response (`AIResponseParser`).
            6.  (Planned) Update local files (`FileUpdater`).
        *   Sets up application-wide logging.
    *   **Dependencies:** `ProjectManager`, `PromptFormatter`, `GeminiClient`, (future: `AIResponseParser`, `FileUpdater`).

*   **`src/project_manager.py` -> `ProjectManager` class:**
    *   **Purpose:** Handles loading, storage, and retrieval of project files (Data I/O Layer).
    *   **Responsibilities:**
        *   Scans a specified project directory for relevant files.
        *   Currently loads `.py` files and a `docs.md` file (if present in the project root).
        *   Ignores common system/VCS directories (e.g., `.git`, `__pycache__`, `venv`).
        *   Stores file content (relative path -> content string) in an internal dictionary.
        *   Provides methods to access loaded file content.
    *   **Dependencies:** `os`, `logging`.

*   **`src/prompt_formatter.py` -> `PromptFormatter` class:**
    *   **Purpose:** Constructs the complete prompt for the AI model, including system instructions, project context, and user-specific tasks.
    *   **Responsibilities:**
        *   Loads a system prompt from an external file (e.g., `prompts/system_json_response_schema.txt`). This system prompt instructs the AI on the expected JSON response format.
        *   Formats Python files from `ProjectManager` as Markdown code blocks.
        *   Attaches `docs.md` content as a separate `google.generativeai.types.Part` if available.
        *   Combines the system prompt, formatted project context, and user instruction into a single string for the AI.
    *   **Dependencies:** `os`, `logging`, `google.generativeai.types.Part`.

*   **`src/gemini_client.py` -> `GeminiClient` class:**
    *   **Purpose:** Manages communication with the Google Gemini AI API (AI Communication Layer).
    *   **Responsibilities:**
        *   Handles API key authentication (reads `GOOGLE_API_KEY` environment variable).
        *   Initializes the Gemini generative model (e.g., `gemini-pro`).
        *   Provides a method (`send_request`) to send the formatted prompt (main string + attachments) to the AI and retrieve the raw text response.
        *   Provides a method (`count_prompt_tokens`) to count tokens for a given prompt and attachments.
    *   **Dependencies:** `os`, `logging`, `google.generativeai`.

*   **`src/ai_response_parser.py` -> `AIResponseParser` class (PLANNED):**
    *   **Purpose:** To parse the raw JSON response from the AI model and transform it into a usable internal representation.
    *   **Responsibilities (Anticipated):**
        *   Receive the raw string response from `GeminiClient`.
        *   Attempt to parse the string as a JSON object.
        *   Validate the JSON structure against the schema defined in the system prompt (e.g., presence of `changes`, `filePath`, `action`, `content` fields).
        *   Handle parsing errors if the AI's response is not valid JSON or does not conform to the schema.
        *   Extract file modification instructions (file path, action, new content) and any errors/notes from the AI.
        *   Return a structured representation of the AI's intended changes.
    *   **Dependencies:** `json`, `logging`.

*   **`src/file_updater.py` -> `FileUpdater` class (PLANNED):**
    *   **Purpose:** To apply the changes parsed from the AI's response to the local project files.
    *   **Responsibilities (Anticipated):**
        *   Receive the structured changes from `AIResponseParser`.
        *   For each change:
            *   If `action` is "update" or "create": write the `content` to the specified `filePath`, creating directories if necessary.
            *   If `action` is "delete": remove the specified `filePath`.
        *   Implement safety mechanisms (e.g., backups, user confirmation - future).
        *   Log all file operations.
    *   **Dependencies:** `os`, `logging`.

### 2.2. Data Flow:

1.  `main.py` collects user config and starts `Application`.
2.  `Application` orchestrates:
    a.  `ProjectManager` loads files from `project_path`.
    b.  `PromptFormatter` loads `prompts/system_json_response_schema.txt`, combines it with loaded project files and user instruction to create the final AI prompt.
    c.  `GeminiClient` sends this prompt to the Gemini API.
    d.  `GeminiClient` receives a raw string response (expected to be JSON).
    e.  (PLANNED) `AIResponseParser` parses this JSON string into structured data representing file changes.
    f.  (PLANNED) `FileUpdater` applies these changes to local files.

## 3. AI Interaction Strategy

### 3.1. Prompting:

-   **System Prompt:** A detailed system prompt is loaded from `prompts/system_json_response_schema.txt`. This prompt explicitly defines the required JSON output format, including fields for `summary`, `changes` (with `filePath`, `action`, `content`, `description`), `errors`, and `notes`.
-   **Project Context:** Code files (`.py`) are embedded directly into the prompt as Markdown code blocks. `docs.md` is sent as a separate attachment (`Part`).
-   **User Instruction:** The user's specific task is appended to the prompt.

### 3.2. Expected AI Response Format:

The AI is strictly instructed to return a single, valid JSON object. The schema for this JSON is (simplified):

```json
{
  "summary": "AI's summary of changes.",
  "changes": [
    {
      "filePath": "relative/path/to/file.ext",
      "action": "update" | "create" | "delete",
      "content": "Full new content of the file for 'update' or 'create'",
      "description": "Optional description of file change."
    }
  ],
  "errors": [
    {
      "errorCode": "ERROR_CODE",
      "message": "Error message."
    }
  ],
  "notes": "Optional general notes from AI."
}
```json
The `content` field within the `changes` array is expected to contain the full source code of the file, with Python indentation and formatting preserved (standard JSON string escaping applies).

## 4. Current Status & Next Steps

-   **Implemented:**
    -   Core application structure (`Application`, `ProjectManager`, `PromptFormatter`, `GeminiClient`).
    -   Loading project files.
    -   Loading system prompt from an external file.
    -   Formatting context and sending requests to Gemini API.
    -   Receiving raw AI response.
    -   Basic logging.
-   **Immediate Next Step:**
    -   **Implement `AIResponseParser`:** This class will parse the JSON response from Gemini, validate it against the expected schema, and extract actionable file change information.
-   **Subsequent Steps:**
    -   **Implement `FileUpdater`:** To apply the parsed changes to the local file system.
    -   Add robust error handling throughout the application.
    -   Implement more sophisticated context management (e.g., selecting only relevant files for the AI).
    -   Consider UI/UX improvements beyond simple script execution.
    -   Explore advanced features like version control integration (Git), interactive feedback loops with the AI, and different file update strategies (e.g., diff application).

## 5. Key Configuration / Environment

-   `GOOGLE_API_KEY`: Must be set as an environment variable for `GeminiClient` to authenticate.
-   `project_root_path` (in `main.py`): Path to the target project for AI modification.
-   `prompts/` directory: Expected to be in the `project_root_path` and contain prompt template files (e.g., `system_json_response_schema.txt`).

This document should provide a solid foundation for understanding the project's current state, design decisions, and future direction.