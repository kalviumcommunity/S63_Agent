# core/model_client.py
from typing import Any, Dict, Optional, Union, List

class BaseModelClient:
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_k: int = 40,
        top_p: float = 0.9,
        stop: Optional[Union[str, List[str]]] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> Any:
        raise NotImplementedError

class MockModelClient(BaseModelClient):
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_k: int = 40,
        top_p: float = 0.9,
        stop: Optional[Union[str, List[str]]] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        stop_str = stop if stop else "None"
        fmt_str = response_format if response_format else "None"
        text = f"Mock reply with temperature {temperature}, top_k {top_k}, top_p {top_p}, stop {stop_str}, response_format {fmt_str}."
        usage = {"prompt_tokens": max(1, len(prompt.split())//1), "completion_tokens": max(1, len(text.split())//1)}
        return {"text": text, "usage": usage}

class GeminiModelClient(BaseModelClient):
    def __init__(self, api_key: str = None, model: str = "gemini-1.5-flash"):
        import os
        import google.generativeai as genai
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self._genai = genai
        self._model = genai.GenerativeModel(model)

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_k: int = 40,
        top_p: float = 0.9,
        stop: Optional[Union[str, List[str]]] = None,
        response_format: Optional[str] = None,
        **kwargs
    ) -> Any:
        call_args = {
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "stop": stop
        }
        if response_format:
            call_args["response_format"] = response_format
        resp = self._model.generate_content(prompt, **call_args, **kwargs)
        return resp