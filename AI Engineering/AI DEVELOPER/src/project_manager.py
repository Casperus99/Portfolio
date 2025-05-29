# src/project_manager.py

import os
import logging
from typing import Dict, List, Optional

# Initialize a logger for this module.
logger = logging.getLogger(__name__)

class ProjectManager:
    """
    Manages the loading, storage, and retrieval of project files.
    It scans a specified project directory, loads relevant code and documentation files,
    and provides methods to access their content.
    """

    def __init__(self, project_root_path: str) -> None:
        """
        Initializes the ProjectManager with the project's root path.

        Args:
            project_root_path: The absolute path to the root directory of the project.
        """
        self.project_root_path: str = project_root_path
        self._files: Dict[str, str] = {}  # Private dictionary to store file contents
        logger.info(f"ProjectManager initialized for project: {self.project_root_path}")

    def load_files(self) -> None:
        """
        Loads the content of Python code files (.py) and the documentation file (docs.md)
        from the specified project directory. The docs.md file is loaded only if it is
        located directly in the project's root directory.

        The function ignores common system and version control directories.
        The loaded content is stored in the internal `_files` dictionary.
        """
        logger.info(f"Starting to load project files from: {self.project_root_path}")
        self._files = {}  # Clear previous content before loading
        
        # List of directories to ignore during project scanning to avoid
        # loading unnecessary files (e.g., dependencies, cache, VCS metadata).
        ignored_directories: List[str] = [
            '__pycache__', '.git', '.venv', 'venv', 'node_modules',
            'build', 'dist', '.vscode', '.idea', '.DS_Store' # Added common dev/system ignore files
        ]

        for root, dirs, files in os.walk(self.project_root_path):
            # Modify the 'dirs' list in-place to instruct os.walk to skip specified directories.
            dirs[:] = [d for d in dirs if d not in ignored_directories]

            for file_name in files:
                file_path = os.path.join(root, file_name)
                # Calculate the relative path of the file concerning the project directory.
                # This path will be used as the file identifier in the AI context.
                relative_path = os.path.relpath(file_path, self.project_root_path)

                # Check if the file is a Python code file (.py)
                if file_name.endswith('.py'):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self._files[relative_path] = f.read()
                            logger.debug(f"Successfully loaded Python file: {relative_path}")
                    except Exception as e:
                        # Log file loading errors to inform the user about any issues.
                        logger.error(f"Error loading Python file '{file_path}': {e}")
                # Check if the file is 'docs.md' and if it's located directly
                # in the project's root directory.
                elif file_name == 'docs.md' and root == self.project_root_path:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self._files[relative_path] = f.read()
                            logger.debug(f"Successfully loaded documentation file: {relative_path}")
                    except Exception as e:
                        logger.error(f"Error loading documentation file '{file_path}': {e}")
        logger.info(f"Finished loading project files. Total files loaded: {len(self._files)}")

    def get_file_content(self, relative_path: str) -> Optional[str]:
        """
        Retrieves the content of a specific file by its relative path.

        Args:
            relative_path: The relative path of the file (e.g., 'src/main.py').

        Returns:
            The content of the file as a string, or None if the file is not found.
        """
        content = self._files.get(relative_path)
        if content is None:
            logger.warning(f"Attempted to get content for non-existent file: {relative_path}")
        return content

    def get_all_python_files(self) -> Dict[str, str]:
        """
        Retrieves a dictionary containing only Python code files and their content.

        Returns:
            A dictionary where keys are relative paths to Python files and values are their content.
        """
        return {path: content for path, content in self._files.items() if path.endswith('.py')}

    def get_docs_md_content(self) -> Optional[str]:
        """
        Retrieves the content of the 'docs.md' file.

        Returns:
            The content of 'docs.md' as a string, or None if the file was not loaded.
        """
        return self._files.get('docs.md')