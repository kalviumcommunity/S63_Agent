import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.base_agent import BaseAgent
from core.model_client import MockModelClient

def test_temperature_effect():
    # Mock client to observe temperature usage
    mock_client = MockModelClient()

    low_temp_agent = BaseAgent(client=mock_client, temperature=0.1)
    high_temp_agent = BaseAgent(client=mock_client, temperature=0.9)

    low_resp = low_temp_agent.ask("Generate a creative sentence.")
    high_resp = high_temp_agent.ask("Generate a creative sentence.")

    print("Low temperature response:", low_resp)
    print("High temperature response:", high_resp)

    assert "0.1" in low_resp, "Low temperature not passed correctly"
    assert "0.9" in high_resp, "High temperature not passed correctly"

if __name__ == "__main__":
    test_temperature_effect()
    print("Temperature test passed!")