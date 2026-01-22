# 🤖 AgentCLI – AI Agents in Your Terminal

AgentCLI is a modular command-line tool that lets you run AI agents directly from your terminal. Built around **Google’s Gemini API**, it enables document-grounded question answering, summarization, and task-based automation over local files — without relying on heavyweight frameworks like LangChain.

The project is designed to be lightweight, extensible, and developer-friendly, focusing on clarity and control rather than hidden abstractions.

---

## 🎯 Target Audience

AgentCLI is built for developers, students, and power users who want to experiment with AI agents locally, understand how they work under the hood, and integrate LLM capabilities into CLI workflows.

---

## 🧠 Project Overview

AgentCLI is a lightweight framework for **developing and running task-specific AI agents**. Each agent is responsible for a single category of task and follows a shared interface, making the system easy to extend.

Core ideas behind the project:

- Direct use of **Gemini’s generative capabilities** for reasoning and text understanding  
- **Document-grounded interaction** by injecting local file content into prompts  
- Clear separation between agents, model clients, and the CLI layer  
- No dependency on orchestration frameworks like LangChain  

---

## 🚀 Features

- Run task-specific agents directly from the terminal
- Ask questions over local files (PDF, TXT, MD)
- Summarize and analyze documents
- Modular, plug-and-play agent architecture
- Pluggable model backends (real API or mock client)
- Lightweight and minimal dependencies

---

## 🏗 Architecture Overview

AgentCLI follows a clean, modular architecture:

- **CLI Layer** – Handles command parsing and user interaction using `argparse`
- **Agent Layer** – Task-specific agents (FileAgent, TutorAgent, SummarizerAgent, etc.)
- **Model Layer** – Interchangeable model clients (Gemini API or MockModelClient)
- **Context Layer** – Injects file content into prompts for document-aware reasoning

This design allows seamless switching between real LLM calls and mocked responses for testing and demos.

---

## 🧪 Mock vs Gemini Mode

AgentCLI supports two interchangeable model backends:

- **GeminiModelClient** – Uses the real Gemini API for production usage
- **MockModelClient** – Used for local testing and demos when API quotas or rate limits are an issue

Both clients implement the same interface, ensuring identical behavior across environments without changing agent logic.

---

## 🔧 Installation

```bash
git clone https://github.com/your-username/agentcli.git
cd agentcli
pip install -r requirements.txt
```

---

## 🔑 API Setup (Gemini)

1. Generate an API key from Google AI Studio:  
   https://aistudio.google.com/app/apikey
2. Set the API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## 💻 Usage

Run agents and ask questions using simple CLI commands:

```bash
# Run a reminder agent on a document
python agentcli.py run ReminderAgent --file report.pdf

# Run a tutor agent with difficulty level
python agentcli.py run TutorAgent --file notes.md --level beginner

# Ask questions about a file
python agentcli.py ask FileAgent "What’s the due date for the project?" --file tasks.txt
```

---

## 📄 Logs & Output

- All interactions are logged to `logs/agentcli.log`
- Results are printed to the terminal
- Outputs can optionally be saved using `--output result.txt`

---

## 🧩 Example Commands

```bash
# Extract deadlines from a PDF
python agentcli.py ask FileAgent "List all deadlines in the document" --file syllabus.pdf

# Summarize a markdown file
python agentcli.py run SummarizerAgent --file notes.md

# Generate reminders from a task list
python agentcli.py run ReminderAgent --file tasks.txt
```

---

## 👤 Author

Created by Hasan