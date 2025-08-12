import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.base_agent import BaseAgent
from core.model_client import MockModelClient

def test_function_calling():
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

    agent = BaseAgent(
        client=MockModelClient(),
        functions=mock_functions,
        function_call={"name": "get_weather"}
    )

    response = agent.ask("What's the weather in Paris?")
    print("Function calling response:", response)

    assert "get_weather" in response, "Function name not found in mock response"
    assert "functions" in response.lower(), "Functions info not reflected in mock output"

if __name__ == "__main__":
    test_function_calling()
    print("Function calling test passed!")