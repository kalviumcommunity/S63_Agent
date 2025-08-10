import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.base_agent import BaseAgent
from core.model_client import MockModelClient

def test_stop_sequence_effect():
    mock_client = MockModelClient()

    stop_agent_1 = BaseAgent(client=mock_client, stop=["\n"])
    stop_agent_2 = BaseAgent(client=mock_client, stop=["###"])

    resp1 = stop_agent_1.ask("Generate a sentence.")
    resp2 = stop_agent_2.ask("Generate a sentence.")

    print("Stop sequence ['\\n'] response:", resp1)
    print("Stop sequence ['###'] response:", resp2)

    assert "\\n" in resp1, "Stop sequence '\\n' not passed correctly"
    assert "###" in resp2, "Stop sequence '###' not passed correctly"

if __name__ == "__main__":
    test_stop_sequence_effect()
    print("Stop sequence test passed!")