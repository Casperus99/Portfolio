import logging
from pathlib import Path

# Import the new facade function from the package
from project_prompt_builder import build_project_prompt # Simplified import

# Configure logger for this module
logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
# IMPORTANT: Define the absolute path to your project directory here.
# Example for Windows: PROJECT_ROOT_PATH = "C:\\Users\\YourUser\\Documents\\my_python_project"
# Example for Linux/macOS: PROJECT_ROOT_PATH = "/home/youruser/my_python_project"
PROJECT_ROOT_PATH = "D:\\GiT\\Portfolio\\AI Engineering\\Flashcard App" # <<< ZMIEŃ TĘ ŚCIEŻKĘ NA WŁAŚCIWĄ!

# Define the name of the directory where input prompt templates are stored
INPUT_PROMPTS_DIR_NAME = "input_prompts"
# Define the name of the full prompt template file
FULL_PROMPT_TEMPLATE_FILE_NAME = "full_prompt_template.md"

# Define the name of the directory where generated prompts are stored
OUTPUT_PROMPTS_DIR_NAME = "output_prompts"
# Define the name of the output file for the generated prompt
GENERATED_PROMPT_OUTPUT_FILE_NAME = "final_prompt.md"
# --- END CONFIGURATION ---

# Default content for the full prompt template.
# This will be created if the template file does not exist.
DEFAULT_FULL_PROMPT_TEMPLATE_CONTENT = """## Project Context Overview ##
Hello Gemini,

You are being provided with a comprehensive overview of a Python project. This context is crucial for any subsequent tasks or questions I might pose regarding the codebase, architecture, or documentation.

Please review the following sections thoroughly:
1.  **Project Directory Structure:** A visual representation of the project's file and folder hierarchy.
2.  **Source Code Section:** The complete source code of all Python files found within the project, each clearly labeled with its relative path.
3.  **Additional Documentation:** A project documentation file (e.g., README.md) has been provided separately for your reference.

I will follow up with specific questions or tasks after you have assimilated this foundational information.

{{PROJECT_CONTEXT}}
"""

def _ensure_input_prompts_directory_and_template_exist(input_prompts_dir: Path, template_path: Path):
    """
    Ensures the 'input_prompts' directory exists and creates a default full prompt template
    if it does not already exist.
    """
    input_prompts_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured input prompts directory exists: {input_prompts_dir}")

    if not template_path.exists():
        try:
            with open(template_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_FULL_PROMPT_TEMPLATE_CONTENT)
            logger.info(f"Created default full prompt template: {template_path}")
            print(f"\n--- Info: Created default template file: {template_path} ---")
            print("You can modify this file to customize your full prompt structure.")
            print("----------------------------------------------------------------")
        except IOError as e:
            logger.error(f"Failed to create default full prompt template {template_path}: {e}")
            print(f"\n--- Error: Failed to create default template file {template_path}: {e} ---")
            print("Please check directory permissions.")
            exit(1) # Exit if we can't even set up the template

def _ensure_output_directory_exists(output_dir: Path):
    """
    Ensures the 'output_prompts' directory exists.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured output prompts directory exists: {output_dir}")


def main():
    """
    Main entry point for the script. Handles file I/O and orchestrates the prompt generation
    using the project_prompt_builder package.
    """
    # Configure basic logging for console output
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Get the directory where the main script is located
    script_dir = Path(__file__).parent
    
    # Define full paths for input/output directories and files
    input_prompts_dir = script_dir / INPUT_PROMPTS_DIR_NAME
    full_prompt_template_path = input_prompts_dir / FULL_PROMPT_TEMPLATE_FILE_NAME
    
    output_prompts_dir = script_dir / OUTPUT_PROMPTS_DIR_NAME
    generated_prompt_output_path = output_prompts_dir / GENERATED_PROMPT_OUTPUT_FILE_NAME

    # Validate the configured project path before proceeding
    if PROJECT_ROOT_PATH == "/path/to/your/project":
        logger.error("Error: Please update the 'PROJECT_ROOT_PATH' variable in main.py "
                     "with the actual absolute path to your project directory.")
        print("\n--- Configuration Error ---")
        print("Please open 'main.py' and set the 'PROJECT_ROOT_PATH' variable "
              "to the absolute path of your Python project.")
        print("Example: PROJECT_ROOT_PATH = \"C:\\Users\\YourUser\\Documents\\my_python_project\"")
        print("Example: PROJECT_ROOT_PATH = \"/home/youruser/my_python_project\"")
        print("---------------------------")
        return

    # Ensure the input prompts directory and template file exist
    _ensure_input_prompts_directory_and_template_exist(input_prompts_dir, full_prompt_template_path)
    
    # Ensure the output directory exists
    _ensure_output_directory_exists(output_prompts_dir)

    # Read the full prompt template content
    try:
        full_prompt_template_content = full_prompt_template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.error(f"Full prompt template file not found: {full_prompt_template_path}. Exiting.")
        print(f"\n--- Error: Full prompt template file not found: {full_prompt_template_path} ---")
        print("Please ensure the template file exists or was created successfully on first run.")
        return
    except Exception as e:
        logger.error(f"Error reading full prompt template file {full_prompt_template_path}: {e}")
        print(f"\n--- Error: Failed to read template file {full_prompt_template_path}: {e} ---")
        return

    # --- Simplified prompt generation using the facade function ---
    generated_prompt = build_project_prompt(
        project_path_str=PROJECT_ROOT_PATH,
        full_prompt_template_str=full_prompt_template_content
    )
    # --- End of simplified generation ---

    # Output the result to a file
    if generated_prompt:
        try:
            with open(generated_prompt_output_path, "w", encoding="utf-8") as f:
                f.write(generated_prompt)
            print(f"\n--- Gemini AI Prompt Content successfully saved to: {generated_prompt_output_path} ---")
            logger.info(f"Prompt content saved to {generated_prompt_output_path}")
        except IOError as e:
            print(f"\n--- Error: Could not write prompt to file {generated_prompt_output_path}: {e} ---")
            logger.error(f"Failed to write prompt to {generated_prompt_output_path}: {e}")
    else:
        print("\nNo prompt content was generated. Please check the provided path and logs for errors or warnings.")
        logger.warning("No prompt content generated, therefore no file was created.")

if __name__ == "__main__":
    main()