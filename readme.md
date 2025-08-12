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

Coming soon....