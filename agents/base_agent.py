import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.model_client import MockModelClient, GeminiModelClient
from core.token_utils import log_tokens

class BaseAgent:
    def __init__(self, client=None, temperature=0.7, top_k=40, top_p=0.9, stop=None, response_format=None, functions=None, function_call=None):
        # Default to GeminiModelClient (real API); pass MockModelClient() for testing
        self.client = client or GeminiModelClient()
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.stop = stop
        self.response_format = response_format
        self.functions = functions
        self.function_call = function_call

    def ask(self, prompt: str):
        resp = self.client.generate(
            prompt,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            stop=self.stop,
            response_format=self.response_format,
            functions=self.functions,
            function_call=self.function_call
        )
        # central token logging
        log_tokens(resp)
        # normalize text return
        if isinstance(resp, dict):
            return resp.get("text") or resp.get("content") or str(resp)
        # if provider object, try attribute access
        return getattr(resp, "text", str(resp))

if __name__ == "__main__":
    mock_functions = [
        {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city"}
                },
                "required": ["city"]
            }
        }
    ]
    # Use MockModelClient to avoid making real API calls during testing
    agent = BaseAgent(
        client=MockModelClient(),  # Use mock client instead of real API
        temperature=0.3,
        top_k=10,
        top_p=0.8,
        stop=["\n", "###"],
        response_format="json",
        functions=mock_functions,
        function_call={"name": "get_weather"}
    )
    answer = agent.ask("What is the weather in Paris?")
    print("Response:", answer)