#!/usr/bin/env python3
"""
AgentCLI - A command-line interface for interacting with AI models
"""

import argparse
import os
import json
import requests
from core.model_client import GeminiModelClient
from core.token_utils import extract_tokens_from_response, log_tokens


def load_prompt_template(mode):
    """Load prompt template based on the selected mode"""
    template_path = f"prompts/{mode}.txt"
    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            return f.read()
    else:
        # Default to zero-shot if template not found
        return "{user_input}"


def process_prompt_with_template(prompt, mode, json_output=False):
    """Process the user prompt with the selected template"""
    template = load_prompt_template(mode)
    processed_prompt = template.format(user_input=prompt)
    
    # If JSON output is requested, wrap the prompt with JSON instructions
    if json_output:
        json_instruction = "\n\nPlease provide your response in valid JSON format."
        processed_prompt = processed_prompt + json_instruction
        
    return processed_prompt


def get_weather_function_schema():
    """Return the function schema for the weather API"""
    return {
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


def get_weather_data(city):
    """Get weather data from OpenWeatherMap API"""
    # Note: In a real implementation, you would need to get an API key from https://openweathermap.org/api
    # and set it as an environment variable OPENWEATHER_API_KEY
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return {"error": "OpenWeatherMap API key not found. Please set OPENWEATHER_API_KEY environment variable."}
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Use Celsius for temperature
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}


def handle_weather_request(city, model_client, **generate_kwargs):
    """Handle weather request by calling the weather API and merging results"""
    # Get weather data
    weather_data = get_weather_data(city)
    
    # If there was an error fetching weather data, return it
    if "error" in weather_data:
        return weather_data["error"]
    
    # Construct function schema for Gemini
    functions = [get_weather_function_schema()]
    function_call = {"name": "get_weather"}
    
    # Create a prompt that includes the weather data
    prompt = f"What is the weather like in {city}? Here is the current weather data: {json.dumps(weather_data)}"
    
    # Call the model with the weather data and function schema
    response = model_client.generate(
        prompt,
        functions=functions,
        function_call=function_call,
        **generate_kwargs
    )
    
    return response


def print_response(response, json_output=False):
    """Print the response, parsing and pretty-printing JSON if requested"""
    response_text = response.text if hasattr(response, 'text') else str(response)
    
    if json_output:
        try:
            # Try to parse the response as JSON and pretty-print it
            parsed_json = json.loads(response_text)
            print(json.dumps(parsed_json, indent=2))
        except json.JSONDecodeError:
            # If JSON parsing fails, print the raw response
            print("Failed to parse response as JSON:")
            print(response_text)
    else:
        print(response_text)


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="AgentCLI - Interact with AI models")
    
    # Add arguments
    parser.add_argument("--prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--mode", type=str, choices=["zero-shot", "one-shot", "multi-shot", "cot", "dynamic"],
                        default="zero-shot", help="Prompt engineering mode")
    parser.add_argument("--json-output", action="store_true", help="Return response in JSON format")
    parser.add_argument("--weather", type=str, help="Get weather for a specific city")
    
    # Model control parameters
    parser.add_argument("--temperature", type=float, help="Temperature for generation (0.0 to 1.0)")
    parser.add_argument("--top-k", type=int, help="Top-K sampling parameter")
    parser.add_argument("--top-p", type=float, help="Top-P sampling parameter")
    parser.add_argument("--stop-sequence", type=str, help="Stop sequence for generation")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Initialize the model client
    model_client = GeminiModelClient()
    
    # If weather flag is provided, handle weather request
    if args.weather:
        # Prepare generation parameters
        generate_kwargs = {}
        if args.temperature is not None:
            generate_kwargs["temperature"] = args.temperature
        if args.top_k is not None:
            generate_kwargs["top_k"] = args.top_k
        if args.top_p is not None:
            generate_kwargs["top_p"] = args.top_p
        if args.stop_sequence is not None:
            generate_kwargs["stop"] = args.stop_sequence
            
        response = handle_weather_request(args.weather, model_client, **generate_kwargs)
        print_response(response, args.json_output)
        
        # Extract and log token information if response is from model
        if hasattr(response, 'text') or isinstance(response, dict):
            tokens = extract_tokens_from_response(response)
            log_tokens(response)
            
            # Append token info to logs/tokens.log
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            
            # Format token information
            token_log = f"[Tokens] Prompt: {tokens['prompt_tokens']}, Completion: {tokens['completion_tokens']}, Total: {tokens['total_tokens']}\n"
            
            # Append to log file
            with open("logs/tokens.log", "a") as f:
                f.write(token_log)
    # If prompt is provided, send it to the model and print the response
    elif args.prompt:
        # Process prompt with selected template
        processed_prompt = process_prompt_with_template(args.prompt, args.mode, args.json_output)
        
        # Prepare generation parameters
        generate_kwargs = {}
        if args.temperature is not None:
            generate_kwargs["temperature"] = args.temperature
        if args.top_k is not None:
            generate_kwargs["top_k"] = args.top_k
        if args.top_p is not None:
            generate_kwargs["top_p"] = args.top_p
        if args.stop_sequence is not None:
            generate_kwargs["stop"] = args.stop_sequence
            
        response = model_client.generate(processed_prompt, **generate_kwargs)
        print_response(response, args.json_output)
        
        # Extract and log token information
        tokens = extract_tokens_from_response(response)
        log_tokens(response)
        
        # Append token info to logs/tokens.log
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Format token information
        token_log = f"[Tokens] Prompt: {tokens['prompt_tokens']}, Completion: {tokens['completion_tokens']}, Total: {tokens['total_tokens']}\n"
        
        # Append to log file
        with open("logs/tokens.log", "a") as f:
            f.write(token_log)
    elif args.interactive:
        print("Interactive mode is not implemented yet.")
    else:
        print("Please provide a prompt using --prompt or use --interactive mode.")


if __name__ == "__main__":
    main()