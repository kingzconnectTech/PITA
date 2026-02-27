import logging
import os
import subprocess
from pita.backend.config.settings import SAFE_PATHS

logger = logging.getLogger("Lucy-FileSystem")

class FileController:
    """
    Handles local file system operations.
    Ensures operations stay within safe paths.
    """
    def __init__(self):
        self.safe_paths = SAFE_PATHS
        logger.info("File Controller initialized.")

    def open_folder(self, target: str) -> str:
        """Safely opens a folder by name or path."""
        # Resolve 'projects' to a real path
        resolved_path = os.path.join(self.safe_paths[0], target)
        
        logger.info(f"Opening folder: '{resolved_path}'")
        
        if os.path.exists(resolved_path):
            if os.name == 'nt': # Windows
                os.startfile(resolved_path)
            else: # macOS/Linux
                subprocess.Popen(['open', resolved_path])
            return f"Opening your '{target}' folder."
        else:
            return f"Error: Folder '{target}' not found."

    def create_folder(self, name: str, parent_path: str = None) -> str:
        """Creates a new folder safely."""
        path = os.path.join(parent_path or self.safe_paths[0], name)
        logger.info(f"Creating folder: '{path}'")
        os.makedirs(path, exist_ok=True)
        return f"Folder '{name}' created."
