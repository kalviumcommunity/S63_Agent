import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.model_client import MockModelClient, GeminiModelClient
from core.token_utils import log_tokens

class BaseAgent:
    def __init__(self, client=None):
        # Default to GeminiModelClient (real API); pass MockModelClient() for testing
        self.client = client or GeminiModelClient()

    def ask(self, prompt: str):
        resp = self.client.generate(prompt)
        # central token logging
        log_tokens(resp)
        # normalize text return
        if isinstance(resp, dict):
            return resp.get("text") or resp.get("content") or str(resp)
        # if provider object, try attribute access
        return getattr(resp, "text", str(resp))

if __name__ == "__main__":
    # Uses GeminiModelClient by default; pass MockModelClient() only for testing without API
    agent = BaseAgent()
    answer = agent.ask("Explain what tokens are in AI models.")
    print("Response:", answer)