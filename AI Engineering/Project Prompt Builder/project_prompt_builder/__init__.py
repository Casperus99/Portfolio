# project_prompt_builder/__init__.py
import logging
from pathlib import Path

# Import the core components
from .project_manager import ProjectManager
from .prompt_formatter import PromptFormatter
from .prompt_generator import PromptGenerator

# Configure logger for this module (optional, as main() configures root logger)
logger = logging.getLogger(__name__)

# Expose key classes for direct import if needed, though facade is preferred for simplicity
__all__ = ["ProjectManager", "PromptFormatter", "PromptGenerator", "build_project_prompt"]


def build_project_prompt(project_path_str: str, full_prompt_template_str: str) -> str:
    """
    A facade function to generate a complete AI prompt for a given project.
    It encapsulates the instantiation and orchestration of internal components.

    Args:
        project_path_str: The string representation of the absolute path to the project directory.
        full_prompt_template_str: The content of the full prompt template as a string,
                                  expected to contain the '{{PROJECT_CONTEXT}}' placeholder.

    Returns:
        A single string containing the fully assembled prompt, or an empty string
        if the project path is invalid or an error occurs during content generation.
    """
    logger.info("Initializing prompt generation process via facade.")
    
    # Instantiate the core components (dependencies)
    project_manager = ProjectManager()
    prompt_formatter = PromptFormatter()

    # Instantiate the prompt generator, injecting its dependencies
    prompt_generator = PromptGenerator(project_manager=project_manager, prompt_formatter=prompt_formatter)

    # Generate the full prompt
    generated_prompt = prompt_generator.generate_full_prompt(
        project_path_str=project_path_str,
        full_prompt_template_str=full_prompt_template_str
    )
    
    logger.info("Prompt generation process completed via facade.")
    return generated_prompt