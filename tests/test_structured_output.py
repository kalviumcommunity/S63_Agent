import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.base_agent import BaseAgent
from core.model_client import MockModelClient

def test_structured_output():
    mock_client = MockModelClient()

    agent_json = BaseAgent(client=mock_client, response_format="json")
    agent_xml = BaseAgent(client=mock_client, response_format="xml")

    resp_json = agent_json.ask("Return user details.")
    resp_xml = agent_xml.ask("Return user details.")

    print("JSON format response:", resp_json)
    print("XML format response:", resp_xml)

    assert "json" in resp_json.lower(), "JSON format not reflected in response"
    assert "xml" in resp_xml.lower(), "XML format not reflected in response"

if __name__ == "__main__":
    test_structured_output()
    print("Structured output test passed!")