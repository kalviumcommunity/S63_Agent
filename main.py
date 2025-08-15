#!/usr/bin/env python3
"""
AgentCLI - A command-line interface for interacting with AI models
"""

import argparse
from core.model_client import GeminiModelClient


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="AgentCLI - Interact with AI models")
    
    # Add arguments
    parser.add_argument("--prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    # Model control parameters
    parser.add_argument("--temperature", type=float, help="Temperature for generation (0.0 to 1.0)")
    parser.add_argument("--top-k", type=int, help="Top-K sampling parameter")
    parser.add_argument("--top-p", type=float, help="Top-P sampling parameter")
    parser.add_argument("--stop-sequence", type=str, help="Stop sequence for generation")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Initialize the model client
    model_client = GeminiModelClient()
    
    # If prompt is provided, send it to the model and print the response
    if args.prompt:
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
            
        response = model_client.generate(args.prompt, **generate_kwargs)
        print(response)
    elif args.interactive:
        print("Interactive mode is not implemented yet.")
    else:
        print("Please provide a prompt using --prompt or use --interactive mode.")


if __name__ == "__main__":
    main()