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
        functions: Optional[List[Dict[str, Any]]] = None,
        function_call: Optional[Union[str, Dict[str, Any]]] = None,
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
        functions: Optional[List[Dict[str, Any]]] = None,
        function_call: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        stop_str = stop if stop else "None"
        fmt_str = response_format if response_format else "None"
        funcs_str = str(functions) if functions else "None"
        func_call_str = str(function_call) if function_call else "None"
        text = (
            f"Mock reply with temperature {temperature}, top_k {top_k}, top_p {top_p}, "
            f"stop {stop_str}, response_format {fmt_str}, functions {funcs_str}, "
            f"function_call {func_call_str}."
        )
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
        functions: Optional[List[Dict[str, Any]]] = None,
        function_call: Optional[Union[str, Dict[str, Any]]] = None,
        **kwargs
    ) -> Any:
        # Create GenerationConfig with the parameters
        generation_config = self._genai.GenerationConfig(
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            stop_sequences=stop if isinstance(stop, list) or stop is None else [stop]
        )
        
        call_args = {
            "generation_config": generation_config
        }
        if response_format:
            call_args["response_format"] = response_format
        if functions:
            call_args["functions"] = functions
        if function_call:
            call_args["function_call"] = function_call
            
        resp = self._model.generate_content(prompt, **call_args, **kwargs)
        return resp