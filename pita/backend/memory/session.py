import logging
from typing import List, Dict

logger = logging.getLogger("Lucy-SessionMemory")

class SessionMemory:
    """
    Handles short-term context.
    Ensures Lucy remembers what you just said.
    """
    def __init__(self):
        self.history: List[Dict[str, str]] = []
        logger.info("Session Memory initialized.")

    def add_interaction(self, user: str, system: str):
        """Adds a turn to the history."""
        self.history.append({"user": user, "system": system})
        if len(self.history) > 10:
            self.history.pop(0)

    def get_context(self) -> str:
        """Returns the context for LLM prompts."""
        context_str = ""
        for turn in self.history:
            context_str += f"User: {turn['user']}\nLucy: {turn['system']}\n"
        return context_str
