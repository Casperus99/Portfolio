import logging
from pathlib import Path
from typing import List

# Import components from the same package
from .project_manager import ProjectManager
from .prompt_formatter import PromptFormatter

logger = logging.getLogger(__name__)

class PromptGenerator:
    """
    Generates a complete AI prompt by combining project context (directory tree, source code)
    with a provided prompt template. This class does not perform file I/O directly for
    templates or output; it operates on strings and Path objects.
    """

    def __init__(self, project_manager: ProjectManager, prompt_formatter: PromptFormatter):
        """
        Initializes the PromptGenerator with necessary dependencies.
        Args:
            project_manager: An instance of ProjectManager for file system operations.
            prompt_formatter: An instance of PromptFormatter for structuring prompt content.
        """
        self.project_manager = project_manager
        self.prompt_formatter = prompt_formatter

    def generate_full_prompt(self, project_path_str: str, full_prompt_template_str: str) -> str:
        """
        Generates the full AI prompt by processing the project and inserting
        the generated context into the provided template string.

        Args:
            project_path_str: The string representation of the absolute path to the project directory.
            full_prompt_template_str: The content of the full prompt template as a string,
                                      expected to contain the '{{PROJECT_CONTEXT}}' placeholder.

        Returns:
            A single string containing the fully assembled prompt, or an empty string
            if the project path is invalid or an error occurs during content generation.
        """
        project_root = Path(project_path_str)

        if not project_root.is_dir():
            logger.error(f"Error: The provided project path '{project_path_str}' is not a valid directory or does not exist.")
            return ""

        # Generate Directory Tree Section
        logger.info(f"Generating directory tree for: {project_root}")
        raw_directory_tree = self.project_manager.get_directory_tree_structure(project_root)
        formatted_directory_tree_section = self.prompt_formatter.format_directory_tree_section(raw_directory_tree)

        # Generate Source Code Section
        logger.info(f"Starting scan for Python files in project directory: {project_root}")
        python_files = self.project_manager.find_python_files(project_root)
        
        formatted_python_parts: List[str] = []
        if not python_files:
            logger.warning(f"No Python files found in '{project_root}' or its subdirectories. Source code section will be empty.")
        else:
            for file_path in python_files:
                try:
                    display_path = file_path.relative_to(project_root)
                except ValueError:
                    display_path = file_path

                logger.info(f"Processing file: {display_path}")
                file_content = self.project_manager.read_file_content(file_path)
                
                if file_content != "":
                    formatted_part = self.prompt_formatter.format_python_file_for_prompt(
                        project_root=project_root,
                        file_path=file_path,
                        file_content=file_content
                    )
                    formatted_python_parts.append(formatted_part)
                else:
                    logger.warning(f"Skipping file {file_path} due to empty content or read error.")
        
        formatted_source_code_section = self.prompt_formatter.format_source_code_section(formatted_python_parts)

        # Combine dynamic sections into the PROJECT_CONTEXT placeholder content
        dynamic_project_context = f"{formatted_directory_tree_section}{formatted_source_code_section}"
        
        # Replace the placeholder in the template with the generated dynamic content
        final_prompt = full_prompt_template_str.replace("{{PROJECT_CONTEXT}}", dynamic_project_context)
        
        logger.info("Successfully assembled full prompt content.")
        return final_prompt