#!/usr/bin/env python3
"""
AgentCLI - A command-line interface for interacting with AI models
"""

import argparse
import os
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


def process_prompt_with_template(prompt, mode):
    """Process the user prompt with the selected template"""
    template = load_prompt_template(mode)
    return template.format(user_input=prompt)


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="AgentCLI - Interact with AI models")
    
    # Add arguments
    parser.add_argument("--prompt", type=str, help="The prompt to send to the model")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--mode", type=str, choices=["zero-shot", "one-shot", "multi-shot", "cot", "dynamic"],
                        default="zero-shot", help="Prompt engineering mode")
    
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
        # Process prompt with selected template
        processed_prompt = process_prompt_with_template(args.prompt, args.mode)
        
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
        print(response.text if hasattr(response, 'text') else response)
        
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