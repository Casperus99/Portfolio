import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

class PromptFormatter:
    """
    Formats file content and paths into a specific string structure suitable for AI prompts.
    Adheres to the Single Responsibility Principle by focusing solely on prompt formatting.
    """

    def format_python_file_for_prompt(self, project_root: Path, file_path: Path, file_content: str) -> str:
        """
        Formats a single Python file's path and content into the specified prompt structure.
        The path will be relative to the provided project_root.

        Args:
            project_root: The root directory of the project, used to calculate relative paths.
            file_path: The absolute path to the Python file.
            file_content: The content of the Python file.

        Returns:
            A formatted string for the AI prompt.
        """
        try:
            relative_path = file_path.relative_to(project_root)
        except ValueError:
            logger.warning(
                f"File path '{file_path}' is not relative to project root '{project_root}'. "
                "Using absolute path for formatting."
            )
            relative_path = file_path

        formatted_string = (
            f"Relative path: {relative_path}\n"
            f"```python\n"
            f"{file_content}\n"
            f"```\n"
        )
        return formatted_string

    def format_source_code_section(self, formatted_parts: List[str]) -> str:
        """
        Combines a list of formatted Python file parts into a single string
        and wraps it with an H2 source code section title.

        Args:
            formatted_parts: A list of strings, where each string is a formatted Python file segment.

        Returns:
            A single concatenated string containing all formatted parts, enclosed
            within a source code section title.
        """
        if not formatted_parts:
            logger.info("No formatted source code parts to combine. Returning an empty string for the section.")
            return ""
        
        section_title = "## Source Code Section ##\n\n"
        combined_content = "".join(formatted_parts)
        
        return f"{section_title}{combined_content}"

    def format_directory_tree_section(self, tree_content: str) -> str:
        """
        Wraps the directory tree content with an H2 section title and triple backticks.

        Args:
            tree_content: The string representation of the directory tree.

        Returns:
            A formatted string for the directory tree section.
        """
        if not tree_content:
            logger.info("No directory tree content provided. Returning an empty string for the section.")
            return ""

        section_title = "## Project Directory Structure ##\n\n"
        formatted_tree = f"```\n{tree_content}\n```\n\n"
        
        return f"{section_title}{formatted_tree}"