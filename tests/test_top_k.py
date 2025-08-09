import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.base_agent import BaseAgent
from core.model_client import MockModelClient

def test_top_k_effect():
    mock_client = MockModelClient()

    low_top_k_agent = BaseAgent(client=mock_client, top_k=5)
    high_top_k_agent = BaseAgent(client=mock_client, top_k=50)

    low_resp = low_top_k_agent.ask("Generate a creative sentence.")
    high_resp = high_top_k_agent.ask("Generate a creative sentence.")

    print("Low top_k response:", low_resp)
    print("High top_k response:", high_resp)

    assert "5" in low_resp, "Low top_k not passed correctly"
    assert "50" in high_resp, "High top_k not passed correctly"

if __name__ == "__main__":
    test_top_k_effect()
    print("Top_k test passed!")