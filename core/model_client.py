# core/model_client.py
from typing import Any, Dict

class BaseModelClient:
    def generate(self, prompt: str, temperature: float = 0.7, top_k: int = 40, **kwargs) -> Any:
        raise NotImplementedError

class MockModelClient(BaseModelClient):
    def generate(self, prompt: str, temperature: float = 0.7, top_k: int = 40, **kwargs) -> Dict[str, Any]:
        # fake response shaped like OpenAI-style usage
        text = f"This is a mock reply for demo purposes with temperature {temperature} and top_k {top_k}."
        usage = {"prompt_tokens": max(1, len(prompt.split())//1), "completion_tokens": max(1, len(text.split())//1)}
        return {"text": text, "usage": usage}

class GeminiModelClient(BaseModelClient):
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        import os
        import google.generativeai as genai
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self._genai = genai
        self._model = genai.GenerativeModel(model)

    def generate(self, prompt: str, temperature: float = 0.7, top_k: int = 40, **kwargs) -> Any:
        # pass temperature and top_k as parameters to the API call
        resp = self._model.generate_content(prompt, temperature=temperature, top_k=top_k, **kwargs)
        return resp