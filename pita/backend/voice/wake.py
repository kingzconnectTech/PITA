import re

class WakeWordDetector:
    def __init__(self, wake_word: str):
        self.pattern = re.compile(r"\b" + re.escape(wake_word.lower()) + r"\b")

    def has_wake_word(self, text: str) -> bool:
        if not text:
            return False
        return bool(self.pattern.search(text.lower()))
