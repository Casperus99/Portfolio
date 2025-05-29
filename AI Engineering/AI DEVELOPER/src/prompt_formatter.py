# src/prompt_formatter.py

import logging
import os # Added for path operations
from typing import Dict, List, Optional, Tuple

# The Part type is necessary for defining the type of attachments for the Gemini API.
from google.generativeai.types import Part

# Initialize a logger for this module.
logger = logging.getLogger(__name__)

class PromptFormatter:
    """
    Responsible for constructing the full prompt and managing attachments
    for the Google Gemini API. It loads a system prompt defining the expected
    response format, then formats project context (code and documentation)
    along with user instructions into a structure suitable for AI consumption.
    """

    # Default filename for the system prompt that defines the JSON response schema.
    DEFAULT_SYSTEM_PROMPT_FILENAME = "system_json_response_schema.txt"

    def __init__(self, prompts_dir_path: str) -> None:
        """
        Initializes the PromptFormatter instance.

        Args:
            prompts_dir_path: The absolute path to the directory containing prompt template files.
        """
        self.prompts_dir_path = prompts_dir_path
        logger.info(f"PromptFormatter initialized. Prompts directory: {self.prompts_dir_path}")

    def _load_prompt_from_file(self, filename: str) -> Optional[str]:
        """
        Loads a prompt template from a specified file within the prompts directory.

        Args:
            filename: The name of the file (e.g., "system_json_response_schema.txt")
                      located in the `self.prompts_dir_path`.

        Returns:
            The content of the file as a string, or None if the file cannot be loaded.
        """
        prompt_file_path = os.path.join(self.prompts_dir_path, filename)
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                prompt_content = f.read()
            logger.debug(f"Successfully loaded prompt from file: {prompt_file_path}")
            return prompt_content
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {prompt_file_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading prompt file '{prompt_file_path}': {e}", exc_info=True)
            return None

    def format_context(self,
                       python_files: Dict[str, str],
                       docs_md_content: Optional[str],
                       user_instruction: str,
                       system_prompt_filename: Optional[str] = None
                       ) -> Tuple[Optional[str], List[Part]]:
        """
        Prepares the system instructions, project context, and user instruction
        for submission to the Google Gemini model.
        Python code files are formatted as Markdown code blocks within the main prompt string.
        The documentation file (docs.md) is attached as a separate Part object.
        A system prompt defining the expected JSON response structure is loaded from a file.

        Args:
            python_files: A dictionary where keys are relative paths to Python files
                          and values are their content.
            docs_md_content: The content of 'docs.md' as a string, or None if not available.
            user_instruction: The specific instruction from the user for the AI model.
            system_prompt_filename: Optional. The filename of the system prompt to load.
                                    Defaults to `DEFAULT_SYSTEM_PROMPT_FILENAME`.

        Returns:
            A tuple containing:
            1. The main prompt string (including system instructions, project context,
               and user instruction), or None if the system prompt cannot be loaded.
            2. A list of Part objects, containing the docs.md file (if it exists).
        """
        logger.info("Starting to format project context and user instruction for Gemini API.")

        # Determine the system prompt filename to use
        actual_system_prompt_filename = system_prompt_filename or self.DEFAULT_SYSTEM_PROMPT_FILENAME

        # Step 1: Load the system prompt that defines the expected JSON response structure.
        system_prompt_content = self._load_prompt_from_file(actual_system_prompt_filename)
        if system_prompt_content is None:
            logger.error(f"Critical: System prompt '{actual_system_prompt_filename}' could not be loaded. Cannot format context.")
            return None, [] # Return None for prompt string if system prompt is missing

        main_prompt_segments: List[str] = []
        gemini_attachments: List[Part] = []

        # Add the loaded system prompt first.
        main_prompt_segments.append(system_prompt_content)
        main_prompt_segments.append("\n--- Project Context Start ---") # Separator
        main_prompt_segments.append("The following are the project's source code files:")

        # Iterate through Python files and format them as Markdown code blocks.
        if python_files:
            for relative_path, content in python_files.items():
                # Ensure content is properly escaped for Markdown, though for Python code blocks
                # it's usually fine. The main concern is the ``` itself.
                # For simplicity, assuming content does not contain ```.
                main_prompt_segments.append(f"\n### File: {relative_path}\n```python\n{content}\n```")
                logger.debug(f"Added Python file to main prompt: {relative_path}")
        else:
            logger.warning("No Python files provided for context.")

        # Handle the documentation file (docs.md) as a separate attachment.
        if docs_md_content:
            # Inform the AI that docs.md is attached, as per previous logic
            main_prompt_segments.append(f"\n--- Project documentation 'docs.md' has been attached as a separate component. Please refer to it as needed. ---")
            # Create a Part object for the documentation content
            try:
                docs_part = Part.from_text(docs_md_content)
                gemini_attachments.append(docs_part)
                logger.debug("Added documentation file as attachment: docs.md")
            except Exception as e: # Catch potential errors from Part.from_text
                logger.error(f"Failed to create Part from docs_md_content: {e}", exc_info=True)

        else:
            logger.info("No 'docs.md' file content provided to attach.")

        main_prompt_segments.append("\n--- Project Context End ---\n")

        # Add the user's specific instruction after the project context.
        main_prompt_segments.append("--- User Instruction Start ---")
        main_prompt_segments.append(user_instruction)
        main_prompt_segments.append("--- User Instruction End ---")

        # Join all segments of the main prompt into a single string.
        main_prompt_string = "\n".join(main_prompt_segments)

        logger.info("Finished formatting project context and user instruction.")
        logger.debug(f"Main prompt length: {len(main_prompt_string)} characters.")
        logger.debug(f"Number of Gemini attachments: {len(gemini_attachments)}")

        return main_prompt_string, gemini_attachments