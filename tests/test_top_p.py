import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.base_agent import BaseAgent
from core.model_client import MockModelClient

def test_top_p_effect():
    mock_client = MockModelClient()

    low_top_p_agent = BaseAgent(client=mock_client, top_p=0.5)
    high_top_p_agent = BaseAgent(client=mock_client, top_p=0.95)

    low_resp = low_top_p_agent.ask("Generate a creative sentence.")
    high_resp = high_top_p_agent.ask("Generate a creative sentence.")

    print("Low top_p response:", low_resp)
    print("High top_p response:", high_resp)

    assert "0.5" in low_resp, "Low top_p not passed correctly"
    assert "0.95" in high_resp, "High top_p not passed correctly"

if __name__ == "__main__":
    test_top_p_effect()
    print("Top_p test passed!")