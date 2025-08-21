#!/usr/bin/env python3
"""
AgentCLI - A command-line interface for interacting with AI models
"""

import argparse
import os
import json
import pickle
import requests
import csv
import time
from core.model_client import GeminiModelClient
from core.token_utils import extract_tokens_from_response, log_tokens
from core.embedding_client import GeminiEmbeddingClient
from core.vector_store import InMemoryVectorStore
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint


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


def load_vector_store():
    """Load vector store from file or create a new one"""
    try:
        with open("vector_db.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return InMemoryVectorStore()


def save_vector_store(vector_store):
    """Save vector store to file"""
    with open("vector_db.pkl", "wb") as f:
        pickle.dump(vector_store, f)


def handle_embed_request(text, embedding_client):
    """Handle embedding request by creating and storing embeddings"""
    # Load existing vector store
    vector_store = load_vector_store()
    
    # Generate embedding for the text
    response = embedding_client.embed([text])
    embedding = response["embeddings"][0]
    
    # Store the embedding in the vector store
    vector_store.upsert_embeddings([text], [embedding])
    
    # Save the updated vector store
    save_vector_store(vector_store)
    
    # Log token usage
    tokens = extract_tokens_from_response(response)
    log_tokens(response)
    
    return f"Successfully embedded and stored text: {text}", tokens


def handle_search_request(query, embedding_client, metric="cosine", k=5):
    """Handle search request by finding nearest matches"""
    # Load vector store
    vector_store = load_vector_store()
    
    # Generate embedding for the query
    response = embedding_client.embed([query])
    query_embedding = response["embeddings"][0]
    
    # Log token usage
    tokens = extract_tokens_from_response(response)
    log_tokens(response)
    
    # Perform similarity search
    results = vector_store.similarity_search(query_embedding, k=k, metric=metric)
    
    return results, tokens


def load_eval_file(file_path):
    """Load evaluation prompts from JSON or CSV file"""
    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            data = json.load(f)
            # If it's a list of prompts, return as is
            if isinstance(data, list):
                return data
            # If it's a dict with a prompts key, return the prompts
            elif isinstance(data, dict) and 'prompts' in data:
                return data['prompts']
            # Otherwise, assume it's a single prompt
            else:
                return [data]
    elif file_path.endswith('.csv'):
        prompts = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Assume the CSV has a 'prompt' column
                if 'prompt' in row:
                    prompts.append(row)
                # If no 'prompt' column, use the first column
                elif row:
                    first_key = next(iter(row))
                    prompts.append({'prompt': row[first_key]})
        return prompts
    else:
        raise ValueError("Unsupported file format. Please provide a JSON or CSV file.")


def run_evaluation(file_path, model_client, embedding_client, **generate_kwargs):
    """Run evaluation on prompts from file and store results"""
    # Load prompts from file
    prompts = load_eval_file(file_path)
    
    # Initialize results list
    results = []
    
    # Run each prompt
    for i, prompt_data in enumerate(prompts):
        try:
            # Handle both string prompts and dict prompts
            if isinstance(prompt_data, str):
                prompt = prompt_data
                mode = "zero-shot"
                json_output = False
            else:
                prompt = prompt_data.get('prompt', '')
                mode = prompt_data.get('mode', 'zero-shot')
                json_output = prompt_data.get('json_output', False)
            
            print(f"Running evaluation {i+1}/{len(prompts)}: {prompt}")
            
            # Process prompt with selected template
            processed_prompt = process_prompt_with_template(prompt, mode, json_output)
            
            # Generate response
            start_time = time.time()
            response = model_client.generate(processed_prompt, **generate_kwargs)
            end_time = time.time()
            
            # Extract response text
            response_text = response.text if hasattr(response, 'text') else str(response)
            
            # Extract token information
            tokens = extract_tokens_from_response(response)
            
            # Create result entry
            result = {
                "id": i+1,
                "input": prompt,
                "mode": mode,
                "output": response_text,
                "tokens": tokens,
                "execution_time": end_time - start_time
            }
            
            results.append(result)
            
            # Log tokens
            log_tokens(response)
            
        except Exception as e:
            # Handle errors
            result = {
                "id": i+1,
                "input": prompt if 'prompt' in locals() else str(prompt_data),
                "mode": mode if 'mode' in locals() else "zero-shot",
                "output": f"Error: {str(e)}",
                "tokens": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                "execution_time": 0
            }
            results.append(result)
            print(f"Error running evaluation {i+1}: {str(e)}")
    
    # Save results to eval_results.json
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results


def print_response(response, json_output=False):
    """Print the response, parsing and pretty-printing JSON if requested"""
    response_text = response.text if hasattr(response, 'text') else str(response)
    
    if json_output:
        try:
            # Try to parse the response as JSON and pretty-print it
            parsed_json = json.loads(response_text)
            rprint("[bold cyan][Response][/bold cyan]")
            print(json.dumps(parsed_json, indent=2))
        except json.JSONDecodeError:
            # If JSON parsing fails, print the raw response
            rprint("[bold red]Failed to parse response as JSON:[/bold red]")
            rprint("[bold cyan][Response][/bold cyan]")
            print(response_text)
    else:
        rprint("[bold cyan][Response][/bold cyan]")
        print(response_text)


def main():
    # Create console instance for rich formatting
    console = Console()
    
    # Display startup banner
    banner = Panel(
        Text("🚀 AgentCLI - Powered by Gemini API", justify="center"),
        border_style="bold blue",
        expand=False
    )
    console.print(banner)
    
    # Create the parser
    parser = argparse.ArgumentParser(description="AgentCLI - Interact with AI models")
    
    # Add arguments
    parser.add_argument("--prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--mode", type=str, choices=["zero-shot", "one-shot", "multi-shot", "cot", "dynamic"],
                        default="zero-shot", help="Prompt engineering mode")
    parser.add_argument("--json-output", action="store_true", help="Return response in JSON format")
    parser.add_argument("--weather", type=str, help="Get weather for a specific city")
    parser.add_argument("--embed", type=str, help="Create and store embeddings for text")
    parser.add_argument("--search", type=str, help="Search for similar texts using embeddings")
    parser.add_argument("--metric", type=str, choices=["cosine", "l2", "dot"], default="cosine",
                        help="Similarity metric for search (cosine, l2, dot)")
    parser.add_argument("--k", type=int, default=5, help="Number of results to return for search")
    parser.add_argument("--eval", type=str, help="Run evaluation on prompts from JSON/CSV file")
    
    # Model control parameters
    parser.add_argument("--temperature", type=float, help="Temperature for generation (0.0 to 1.0)")
    parser.add_argument("--top-k", type=int, help="Top-K sampling parameter")
    parser.add_argument("--top-p", type=float, help="Top-P sampling parameter")
    parser.add_argument("--stop-sequence", type=str, help="Stop sequence for generation")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Initialize the model client
    model_client = GeminiModelClient()
    
    # Initialize the embedding client
    embedding_client = GeminiEmbeddingClient()
    
    # If eval flag is provided, run evaluation
    if args.eval:
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
            
        results = run_evaluation(args.eval, model_client, embedding_client, **generate_kwargs)
        print(f"Evaluation completed. Results saved to eval_results.json")
        rprint(f"[bold magenta][Tokens][/bold magenta] Total tokens used: {sum(r['tokens']['total_tokens'] for r in results)}")
    # If embed flag is provided, handle embedding request
    elif args.embed:
        result, tokens = handle_embed_request(args.embed, embedding_client)
        print(result)
        rprint(f"[bold magenta][Tokens][/bold magenta] Prompt: {tokens['prompt_tokens']}, Completion: {tokens['completion_tokens']}, Total: {tokens['total_tokens']}")
        
        # Append token info to logs/tokens.log
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Format token information
        token_log = f"[Tokens] Embedding operation for text: {args.embed}\n"
        
        # Append to log file
        with open("logs/tokens.log", "a") as f:
            f.write(token_log)
    # If search flag is provided, handle search request
    elif args.search:
        results, tokens = handle_search_request(args.search, embedding_client, args.metric, args.k)
        
        # Print results
        if results:
            print(f"Top {len(results)} results for '{args.search}' using {args.metric} similarity:")
            for i, (score, payload) in enumerate(results, 1):
                print(f"{i}. Score: {score:.4f} - Text: {payload['text']}")
        else:
            print(f"No results found for '{args.search}'")
        
        rprint(f"[bold magenta][Tokens][/bold magenta] Prompt: {tokens['prompt_tokens']}, Completion: {tokens['completion_tokens']}, Total: {tokens['total_tokens']}")
        
        # Append token info to logs/tokens.log
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Format token information
        token_log = f"[Tokens] Search operation for query: {args.search}\n"
        
        # Append to log file
        with open("logs/tokens.log", "a") as f:
            f.write(token_log)
    # If weather flag is provided, handle weather request
    elif args.weather:
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
            rprint(f"[bold magenta][Tokens][/bold magenta] Prompt: {tokens['prompt_tokens']}, Completion: {tokens['completion_tokens']}, Total: {tokens['total_tokens']}")
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
        
        # Display prompt with color
        rprint("[bold green][Prompt][/bold green]")
        print(processed_prompt)
        
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
        rprint(f"[bold magenta][Tokens][/bold magenta] Prompt: {tokens['prompt_tokens']}, Completion: {tokens['completion_tokens']}, Total: {tokens['total_tokens']}")
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