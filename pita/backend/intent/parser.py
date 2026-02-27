import logging
import json
from pita.backend.config.settings import LLM_MODEL, LLM_PROVIDER
from pita.backend.intent.llm_provider import LLMProvider

logger = logging.getLogger("Lucy-IntentParser")

class IntentParser:
    def __init__(self):
        logger.info(f"Intent Parser initialized using {LLM_PROVIDER}:{LLM_MODEL}")
        self.llm = LLMProvider()

    def parse(self, text: str):
        logger.info(f"Parsing: '{text}'")
        sys_prompt = (
            "You convert user text into a JSON object with keys: intent, target, confidence. "
            "Allowed intents: open_folder, browser_search, type_text. "
            "Use short target text only."
        )
        prompt = f"Text: {text}\nReturn JSON."
        result = self.llm.generate_json(prompt, sys_prompt)
        if result.get("intent"):
            return {
                "intent": result.get("intent", "unknown"),
                "target": result.get("target", ""),
                "confidence": self._normalize_confidence(result.get("confidence")),
            }
        
        text = text.lower()
        if "open" in text and "folder" in text:
            return {"intent": "open_folder", "target": "documents", "confidence": 0.95}
        elif "search" in text:
            return {"intent": "browser_search", "target": text.replace("search", "").strip(), "confidence": 0.9}
        elif "type" in text:
            return {"intent": "type_text", "target": text.replace("type", "").strip(), "confidence": 0.85}
        
        return {
            "intent": "unknown",
            "text": text,
            "confidence": 0.0
        }

    def _normalize_confidence(self, value):
        try:
            if value is None:
                return 0.5
            if isinstance(value, (int, float)):
                x = float(value)
                if x > 1:
                    x = x / 100.0
                return max(0.0, min(1.0, x))
            s = str(value).strip().lower()
            if s.endswith("%"):
                return max(0.0, min(1.0, float(s[:-1]) / 100.0))
            mapping = {"low": 0.25, "medium": 0.5, "mid": 0.5, "high": 0.85, "very high": 0.95}
            if s in mapping:
                return mapping[s]
            x = float(s)
            if x > 1:
                x = x / 100.0
            return max(0.0, min(1.0, x))
        except:
            return 0.5
