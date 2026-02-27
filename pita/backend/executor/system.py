import logging
import pyautogui

logger = logging.getLogger("Lucy-SystemControl")

class SystemController:
    """
    Handles keyboard and mouse control.
    """
    def __init__(self):
        pyautogui.FAILSAFE = True
        logger.info("System Controller initialized.")

    def execute_shortcut(self, shortcut: str) -> str:
        """Simulates keyboard shortcuts."""
        logger.info(f"Executing shortcut: '{shortcut}'")
        
        shortcut_map = {
            "copy": ["ctrl", "c"],
            "paste": ["ctrl", "v"],
            "undo": ["ctrl", "z"],
            "save": ["ctrl", "s"],
            "minimize": ["win", "d"]
        }

        keys = shortcut_map.get(shortcut.lower())
        if keys:
            pyautogui.hotkey(*keys)
            return f"Executing shortcut '{shortcut}'."
        else:
            return f"Error: Shortcut '{shortcut}' unknown."

    def type_text(self, text: str) -> str:
        """Simulates typing."""
        logger.info(f"Typing: '{text}'")
        pyautogui.typewrite(text, interval=0.01)
        return "Typed it out for you."
