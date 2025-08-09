# core/model_client.py
from typing import Any, Dict

class BaseModelClient:
    def generate(self, prompt: str, **kwargs) -> Any:
        raise NotImplementedError

class MockModelClient(BaseModelClient):
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        # fake response shaped like OpenAI-style usage
        text = "This is a mock reply for demo purposes."
        usage = {"prompt_tokens": max(1, len(prompt.split())//1), "completion_tokens": max(1, len(text.split())//1)}
        return {"text": text, "usage": usage}

class GeminiModelClient(BaseModelClient):
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        # skeleton: only import when actually used
        import os
        import google.generativeai as genai
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self._genai = genai
        self._model = genai.GenerativeModel(model)

    def generate(self, prompt: str, **kwargs) -> Any:
        # call the real API (example; exact call may vary with lib version)
        resp = self._model.generate_content(prompt, **kwargs)
        return resp