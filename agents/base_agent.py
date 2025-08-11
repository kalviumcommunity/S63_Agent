import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.model_client import MockModelClient, GeminiModelClient
from core.token_utils import log_tokens

class BaseAgent:
    def __init__(self, client=None, temperature=0.7, top_k=40, top_p=0.9, stop=None, response_format=None):
        # Default to GeminiModelClient (real API); pass MockModelClient() for testing
        self.client = client or GeminiModelClient()
        self.temperature = temperature
        self.top_k = top_k
        self.top_p = top_p
        self.stop = stop
        self.response_format = response_format

    def ask(self, prompt: str):
        resp = self.client.generate(
            prompt,
            temperature=self.temperature,
            top_k=self.top_k,
            top_p=self.top_p,
            stop=self.stop,
            response_format=self.response_format
        )
        # central token logging
        log_tokens(resp)
        # normalize text return
        if isinstance(resp, dict):
            return resp.get("text") or resp.get("content") or str(resp)
        # if provider object, try attribute access
        return getattr(resp, "text", str(resp))

if __name__ == "__main__":
    # Uses GeminiModelClient by default; pass MockModelClient() only for testing without API
    agent = BaseAgent(temperature=0.3, top_k=10, top_p=0.8, stop=["\n", "###"], response_format="json")
    answer = agent.ask("Explain what tokens are in AI models.")
    print("Response:", answer)