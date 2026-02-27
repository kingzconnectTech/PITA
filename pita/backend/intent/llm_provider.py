import logging
import json
import ollama
from typing import Dict, Any, Optional
from pita.backend.config.settings import LLM_PROVIDER, LLM_MODEL

logger = logging.getLogger("Lucy-LLM")

class LLMProvider:
    def __init__(self, provider: str = None, model: str = None):
        self.provider = provider or LLM_PROVIDER
        self.model = model or LLM_MODEL
        logger.info(f"LLM Provider initialized: {self.provider} using {self.model}")

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        if self.provider == "ollama":
            return self._generate_ollama(prompt, system_prompt)
        return self._generate_ollama(prompt, system_prompt)

    def _generate_ollama(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            response = ollama.chat(model=self.model, messages=messages)
            return response.get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Ollama Error: {e}")
            return ""

    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        raw = self.generate(prompt, system_prompt)
        try:
            s = raw.strip()
            if "```json" in s:
                s = s.split("```json")[1].split("```")[0].strip()
            elif "```" in s:
                s = s.split("```")[1].split("```")[0].strip()
            if s.startswith("{"):
                end = s.rfind("}")
                if end != -1:
                    s = s[: end + 1]
            return json.loads(s)
        except Exception as e:
            logger.error(f"LLM JSON parse error: {e}")
            return {}
