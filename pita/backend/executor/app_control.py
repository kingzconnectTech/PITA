import logging
import subprocess
from pita.backend.config.settings import ALLOWED_APPLICATIONS

logger = logging.getLogger("Lucy-AppControl")

class AppController:
    """
    Handles launching and managing applications.
    """
    def __init__(self):
        self.allowed_apps = ALLOWED_APPLICATIONS
        logger.info("App Controller initialized.")

    def launch(self, app_name: str) -> str:
        """Launches an app by name."""
        logger.info(f"Launching app: '{app_name}'")
        
        # Simple mapping
        app_map = {
            "code": "code",
            "vscode": "code",
            "browser": "chrome",
            "chrome": "chrome",
            "terminal": "wt"
        }

        executable = app_map.get(app_name.lower(), app_name)
        
        try:
            subprocess.Popen(executable, shell=True)
            return f"Launching {app_name}."
        except Exception as e:
            logger.error(f"Failed to launch {app_name}: {e}")
            return f"Error: Could not launch {app_name}."
