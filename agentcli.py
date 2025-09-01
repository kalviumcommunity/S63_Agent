#!/usr/bin/env python3
"""
AgentCLI - A command-line interface for running AI agents
"""

import argparse
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import print as rprint

# Import agents
from agents.file_agent import FileAgent
from agents.summarizer_agent import SummarizerAgent
from agents.reminder_agent import ReminderAgent
from agents.tutor_agent import TutorAgent

def get_agent_class(agent_name):
    agents = {
        'FileAgent': FileAgent,
        'SummarizerAgent': SummarizerAgent,
        'ReminderAgent': ReminderAgent,
        'TutorAgent': TutorAgent
    }
    if agent_name not in agents:
        raise ValueError(f"Unknown agent: {agent_name}. Available agents: {list(agents.keys())}")
    return agents[agent_name]

def log_to_file(message):
    os.makedirs("logs", exist_ok=True)
    with open("logs/agentcli.log", "a") as f:
        f.write(message + "\n")

def main():
    console = Console()
    
    # Display startup banner
    banner = Panel(
        Text("🚀 AgentCLI - Powered by Gemini API", justify="center"),
        border_style="bold blue",
        expand=False
    )
    console.print(banner)
    
    parser = argparse.ArgumentParser(description="AgentCLI - Run AI agents")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run an agent on a file')
    run_parser.add_argument('agent_name', help='Name of the agent to run')
    run_parser.add_argument('--file', required=True, help='Path to the file to process')
    run_parser.add_argument('--level', default='beginner', help='Level for TutorAgent (beginner, intermediate, advanced)')
    run_parser.add_argument('--output', help='Output file to save results')
    
    # Ask command
    ask_parser = subparsers.add_parser('ask', help='Ask an agent a question about a file')
    ask_parser.add_argument('agent_name', help='Name of the agent to ask')
    ask_parser.add_argument('question', help='Question to ask the agent')
    ask_parser.add_argument('--file', required=True, help='Path to the file to query')
    ask_parser.add_argument('--output', help='Output file to save results')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        agent_class = get_agent_class(args.agent_name)
        
        if args.command == 'run':
            if args.agent_name == 'TutorAgent':
                agent = agent_class(file_path=args.file, level=args.level)
            else:
                agent = agent_class(file_path=args.file)
            result = agent.run()
        elif args.command == 'ask':
            agent = agent_class(file_path=args.file)
            result = agent.ask(args.question)
        
        # Print result
        rprint("[bold cyan][Result][/bold cyan]")
        print(result)
        
        # Save to output file if specified
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"Results saved to {args.output}")
        
        # Log to file
        log_message = f"[{args.command}] {args.agent_name} on {args.file}"
        if args.command == 'ask':
            log_message += f" - Question: {args.question}"
        log_to_file(log_message)
        
    except FileNotFoundError as e:
        rprint(f"[bold red]Error: File not found - {str(e)}[/bold red]")
        rprint("[yellow]Please check the file path and try again.[/yellow]")
        log_to_file(f"File not found: {str(e)}")
        sys.exit(1)
    except ValueError as e:
        rprint(f"[bold red]Error: Invalid input - {str(e)}[/bold red]")
        rprint("[yellow]Please check the agent name and try again.[/yellow]")
        log_to_file(f"Value error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "quota" in error_str.lower():
            rprint("[bold red]Error: API quota exceeded[/bold red]")
            rprint("[yellow]The Gemini API quota has been exceeded. Please try again later or check your API usage limits.[/yellow]")
        elif "403" in error_str:
            rprint("[bold red]Error: API key invalid or unauthorized[/bold red]")
            rprint("[yellow]Please check your GEMINI_API_KEY environment variable or API key permissions.[/yellow]")
        elif "500" in error_str or "502" in error_str or "503" in error_str:
            rprint("[bold red]Error: API server error[/bold red]")
            rprint("[yellow]The Gemini API is experiencing issues. Please try again later.[/yellow]")
        else:
            rprint(f"[bold red]Error: {error_str}[/bold red]")
        log_to_file(f"Error: {error_str}")
        sys.exit(1)

if __name__ == "__main__":
    main()