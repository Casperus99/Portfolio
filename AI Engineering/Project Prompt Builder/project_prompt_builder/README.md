# project_prompt_builder - Package Documentation

## 1. Overview

The `project_prompt_builder` package is a specialized Python tool designed to automate the generation of comprehensive, context-rich prompts for Large Language Models (LLMs), particularly those used in software development and analysis (like Google Gemini).

Its primary goal is to provide an AI model with a structured and detailed understanding of a given Python project's structure and source code. This enables the AI to perform tasks such as code analysis, documentation generation, refactoring suggestions, or bug identification with greater accuracy and awareness.

The package operates on a project's directory path and a user-provided prompt template, returning a single, formatted string ready to be used as input for an AI model.

## 2. Core Concept

The fundamental idea is to bridge the gap between a local project codebase and an AI model's understanding. It achieves this by:

1.  **Scanning:** Analyzing a specified project directory to identify its structure and relevant source files (currently `.py` files).
2.  **Extracting:** Reading the content of these source files.
3.  **Formatting:** Presenting the directory structure and source code in a highly structured, human-readable, and AI-parseable format.
4.  **Injecting:** Inserting this formatted project context into a predefined placeholder (`{{PROJECT_CONTEXT}}`) within a user-supplied prompt template string.

This process results in a complete prompt that sets the stage for the AI, providing it with the necessary background before receiving a specific task.

## 3. Architecture & Design Principles

The package is designed following key Object-Oriented Programming (OOP) principles to ensure modularity, testability, and extensibility:

*   **Single Responsibility Principle (SRP):** Each class has one, clearly defined job.
*   **Loose Coupling:** Components interact through well-defined interfaces (methods) and are largely independent.
*   **Encapsulation:** Internal implementation details are hidden.

The core components are:

*   **`ProjectManager`:**
    *   **Responsibility:** Interacting with the file system.
    *   **Tasks:** Recursively finding Python files (`.py`), generating a visual directory tree (excluding `__pycache__`), and reading the content of individual files. It abstracts away the complexities of file system navigation and access.
*   **`PromptFormatter`:**
    *   **Responsibility:** Structuring and formatting data for the prompt.
    *   **Tasks:** Taking raw data (like the directory tree string or file content) and wrapping it in appropriate Markdown sections (e.g., `## Project Directory Structure ##`, code blocks with language identifiers). It ensures the output is clean and easily digestible by the AI.
*   **`PromptGenerator`:**
    *   **Responsibility:** Orchestrating the prompt generation process.
    *   **Tasks:** It utilizes `ProjectManager` to gather project data and `PromptFormatter` to structure it. It then combines these formatted sections into the final `PROJECT_CONTEXT` block. It *does not* handle template I/O; it expects the template as a string.
*   **`build_project_prompt` (Facade Function):**
    *   **Responsibility:** Providing a simple, high-level public interface to the package's functionality.
    *   **Tasks:** It handles the creation and wiring of the `ProjectManager`, `PromptFormatter`, and `PromptGenerator` instances, hiding this complexity from the end-user.

## 4. Public Interface: The Facade Function

The recommended and simplest way to use this package is through the `build_project_prompt` function, available directly from the package root.

```python
from project_prompt_builder import build_project_prompt

project_path = "/path/to/your/python/project"
template_string = "Here is the project context:\n{{PROJECT_CONTEXT}}\nNow, please analyze it."

final_prompt = build_project_prompt(
    project_path_str=project_path,
    full_prompt_template_str=template_string
)

print(final_prompt)
```

**Arguments:**

*   `project_path_str (str)`: The absolute path to the root directory of the Python project you want to analyze.
*   `full_prompt_template_str (str)`: A string containing the full prompt template. This string *must* include the placeholder `{{PROJECT_CONTEXT}}`, which will be replaced by the generated project information.

**Returns:**

*   `str`: The complete, formatted prompt string, ready to be sent to an AI model. Returns an empty string if an error occurs (e.g., invalid project path).

## 5. Workflow

When `build_project_prompt` is called, the following sequence occurs internally:

1.  The function instantiates `ProjectManager`, `PromptFormatter`, and `PromptGenerator`.
2.  It invokes the `generate_full_prompt` method on the `PromptGenerator` instance, passing the project path and template string.
3.  `PromptGenerator` calls `ProjectManager.get_directory_tree_structure` to get the project hierarchy.
4.  `PromptGenerator` calls `ProjectManager.find_python_files` to get a list of Python files.
5.  `PromptGenerator` iterates through the files, calling `ProjectManager.read_file_content` for each.
6.  `PromptGenerator` calls `PromptFormatter.format_directory_tree_section` to format the tree.
7.  `PromptGenerator` calls `PromptFormatter.format_python_file_for_prompt` for each file and then `PromptFormatter.format_source_code_section` to format the collected code.
8.  `PromptGenerator` concatenates the formatted tree and code sections.
9.  `PromptGenerator` replaces the `{{PROJECT_CONTEXT}}` placeholder in the `full_prompt_template_str` with the concatenated sections.
10. The resulting string is returned by `PromptGenerator` and, subsequently, by `build_project_prompt`.

## 6. Scope & Limitations

It is crucial to understand what this package *does not* do:

*   **No File I/O for Templates/Output:** The `project_prompt_builder` package *itself* does not read prompt templates from files, nor does it write the final prompt to a file. It operates purely on string inputs and returns a string output.
*   **Responsibility of the Caller:** The responsibility of loading the template string (e.g., from a file in `input_prompts/`) and saving the final prompt (e.g., to a file in `output_prompts/`) lies entirely with the *calling script* (like `main.py`). This design ensures the core logic remains decoupled from specific I/O implementations.
*   **Python Only:** Currently, it is designed to process only Python (`.py`) files for the source code section.
*   **No Documentation Parsing:** It does not automatically parse or include project documentation files (like `README.md`) within the prompt, although the template can mention that such files are provided separately.

## 7. Output Format

The `{{PROJECT_CONTEXT}}` placeholder will be replaced with a block containing two main sections:

*   **`## Project Directory Structure ##`**: Contains the project tree, formatted with `├──`, `└──`, and enclosed in ` ``` ` backticks.
*   **`## Source Code Section ##`**: Contains the content of each `.py` file, preceded by its relative path and enclosed in ` ```python ... ``` ` blocks.

This structured output is designed for optimal clarity and parseability by AI models.