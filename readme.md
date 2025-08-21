# 🤖 AgentCLI – AI Agents in Your Terminal

AgentCLI is a modular command-line tool that allows users to interact with powerful AI agents directly from their terminal. Built around the **Gemini API** by Google, AgentCLI enables smart interaction with local documents (like PDFs, text files, and markdown), allowing users to extract actionable insights, answer questions, and perform task-based automation — all with zero reliance on heavyweight frameworks like LangChain.

## 🎯 Target Audience

AgentCLI is designed for developers, researchers, and power users who want to harness AI agents through their terminal without the bloat of large frameworks.

---

## 🧠 Project Idea

AgentCLI is designed as a lightweight and extensible CLI framework for **developing and running AI agents**. Each agent is built to handle a specific category of task using:

- **Gemini’s generative capabilities for text understanding and reasoning**
- **Custom function calls to perform real-world actions**
- **Semantic search and retrieval over local files (RAG)**

## ❓ Why This Project?

In a world dominated by complex orchestration frameworks, AgentCLI brings things back to basics — empowering developers to quickly prototype and run AI agents without hidden abstraction or unnecessary bloat.

## 🚀 Features

- Run task-specific agents directly from the terminal
- Perform semantic search and Q&A over local files (PDF, TXT, MD)
- Leverage function calling to automate tasks
- Modular, plug-and-play agent design — easy to extend
- Lightweight: no LangChain, minimal dependencies

The user runs agents using simple commands like:

```bash
python agentcli.py run ReminderAgent --file report.pdf
python agentcli.py run TutorAgent --file notes.md --level beginner
python agentcli.py ask FileAgent "What’s the due date for the project?" --file tasks.txt
```

## 🔧 Installation

Coming soon...

By Hasan 
# 🤖 AgentCLI – AI Agents in Your Terminal

AgentCLI is a modular command-line tool that brings the power of AI agents directly to your terminal. Built around the **Gemini API** by Google, AgentCLI enables smart interaction with local documents (PDF, TXT, MD), allowing you to extract insights, answer questions, and automate tasks — all without heavyweight frameworks like LangChain.

---

## 🚀 Features

- **Run task-specific agents from the terminal**
- **Semantic search and Q&A over local files (PDF, TXT, MD)**
- **Function calling for task automation**
- **Modular, plug-and-play agent design**
- **Lightweight: no LangChain, minimal dependencies**

---

## 📦 Installation

> **Note:** Installation instructions coming soon!

---

## 🔑 API Setup

1. Obtain your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Set your API key as an environment variable:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

---

## 💻 Usage

Run agents and ask questions using simple commands:

```bash
# Run a reminder agent on a PDF
python agentcli.py run ReminderAgent --file report.pdf

# Run a tutor agent on notes
python agentcli.py run TutorAgent --file notes.md --level beginner

# Ask a file agent a question
python agentcli.py ask FileAgent "What’s the due date for the project?" --file tasks.txt
```

---

## 📄 Logs & Output

- All agent interactions and results are logged to `logs/agentcli.log`.
- Outputs are printed to the terminal and optionally saved to a file with `--output result.txt`.

---

## 🧩 Examples

- **Extract deadlines from a PDF:**  
  ```bash
  python agentcli.py ask FileAgent "List all deadlines in the document" --file syllabus.pdf
  ```
- **Summarize a markdown file:**  
  ```bash
  python agentcli.py run SummarizerAgent --file notes.md
  ```
- **Automate reminders:**  
  ```bash
  python agentcli.py run ReminderAgent --file tasks.txt
  ```

---

## 👤 Author

Created by Hasan