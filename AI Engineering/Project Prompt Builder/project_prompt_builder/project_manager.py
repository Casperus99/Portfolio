import logging
from pathlib import Path
import os
from typing import List, Tuple

logger = logging.getLogger(__name__)

class ProjectManager:
    """
    Manages file system operations, specifically finding and reading Python files,
    and generating the directory tree structure.
    Adheres to the Single Responsibility Principle by focusing solely on file system interactions.
    """

    def find_python_files(self, directory_path: Path) -> List[Path]:
        """
        Recursively finds all Python files (.py) within the specified directory.

        Args:
            directory_path: The root directory to start the search from.

        Returns:
            A list of Path objects, each representing a found Python file.
            Returns an empty list if no .py files are found or the directory is invalid.
        """
        if not directory_path.is_dir():
            logger.error(f"Provided path is not a valid directory: {directory_path}")
            return []

        python_files = []
        try:
            for file_path in directory_path.rglob('*.py'):
                if file_path.is_file():
                    python_files.append(file_path)
        except Exception as e:
            logger.exception(f"An error occurred while searching for Python files in {directory_path}: {e}")
        
        if not python_files:
            logger.warning(f"No Python files (.py) found in directory: {directory_path} or its subdirectories.")

        return python_files

    def read_file_content(self, file_path: Path) -> str:
        """
        Reads the entire content of a specified file.

        Args:
            file_path: The path to the file to read.

        Returns:
            The content of the file as a string.
            Returns an empty string if the file cannot be read or is empty.
        """
        if not file_path.is_file():
            logger.error(f"Provided path is not a valid file or does not exist: {file_path}")
            return ""

        try:
            content = file_path.read_text(encoding='utf-8')
            return content
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return ""
        except UnicodeDecodeError:
            logger.error(f"Could not decode file content as UTF-8. Please check file encoding: {file_path}")
            return ""
        except IOError as e:
            logger.error(f"An I/O error occurred while reading file {file_path}: {e}")
            return ""
        except Exception as e:
            logger.exception(f"An unexpected error occurred while reading file {file_path}: {e}")
            return ""

    def _generate_tree_lines_recursive(self, current_dir: Path, prefix: str, tree_lines: List[str]):
        """
        Recursively generates lines for the directory tree structure, using the
        '├──', '└──', and '│   ' visual style. Excludes '__pycache__' directories.

        Args:
            current_dir: The current directory to process.
            prefix: The string prefix to apply to the current level's items,
                    built from parent's branch indicators.
            tree_lines: The list to append generated tree lines to.
        """
        entries = []
        try:
            for entry in current_dir.iterdir():
                if entry.is_dir() and entry.name == "__pycache__":
                    logger.debug(f"Skipping __pycache__ directory: {entry}")
                    continue

                try:
                    is_dir = entry.is_dir()
                    entries.append((entry, is_dir))
                except OSError:
                    logger.debug(f"Skipping inaccessible entry: {entry}")
                    continue
        except OSError as e:
            logger.warning(f"Could not list directory contents for {current_dir}: {e}")
            return

        entries.sort(key=lambda x: (not x[1], x[0].name.lower()))

        for i, (entry_path, is_dir) in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            next_prefix_extension = "    " if is_last else "│   "
            next_prefix = prefix + next_prefix_extension
            display_name = entry_path.name
            if is_dir:
                display_name += "/"
            
            tree_lines.append(f"{prefix}{connector}{display_name}")

            if is_dir:
                self._generate_tree_lines_recursive(entry_path, next_prefix, tree_lines)

    def get_directory_tree_structure(self, directory_path: Path) -> str:
        """
        Generates a string representation of the directory tree structure,
        including all files and subdirectories, using the `├──`, `└──`, and `│   ` characters.
        Excludes '__pycache__' directories.

        Args:
            directory_path: The root directory to generate the tree from.

        Returns:
            A string representing the directory tree, or an empty string if
            the directory is invalid.
        """
        if not directory_path.is_dir():
            logger.error(f"Provided path is not a valid directory for tree generation: {directory_path}")
            return ""

        tree_lines: List[str] = []
        tree_lines.append(f"{directory_path.name}/")
        self._generate_tree_lines_recursive(directory_path, "", tree_lines)

        if len(tree_lines) == 1 and tree_lines[0] == f"{directory_path.name}/":
            logger.warning(f"Directory '{directory_path}' is empty or only contains the root itself. Tree will be minimal.")

        return "\n".join(tree_lines)