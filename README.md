# RotterMaatje

[![Python](https://img.shields.io/badge/Python->=3.12-blue)](https://www.python.org/)
[![Chainlit](https://img.shields.io/badge/Chainlit-UI-orange)](https://docs.chainlit.io/)

## Description

**RotterMaatje** is an AI-powered chatbot designed for volunteers at [Pauluskerk Rotterdam](https://pauluskerkrotterdam.nl/) to assist "dak- en thuislozen" (homeless individuals) in finding essential services such as shelter, food, socialization opportunities, and medical care. 

The bot provides **accurate, real-time information** aggregated from sources like the Rotterdam municipality, shelter websites, Rode Kruis, Leger des Heils, and more. It features multilingual support (Dutch, English, Polish, Arabic), safety guardrails for emergency detection, and Retrieval-Augmented Generation (RAG) for factual and relevant responses.

Currently in **early development**: Terminal mode fully functional, Web UI (Chainlit) in progress.

## Features

- **Multilingual Support**: Detects and responds in Dutch, English, Polish, Arabic.
- **RAG Knowledge Base**: Vector search (mocked with pgvector-ready skeleton) for shelters, medical services, procedures.
- **AI‑Driven Triage**: Dedicated Pydantic‑AI agent classifies each user input into topic, language, emergency status, and disclaimer level (none/info/caution/urgent). Replaces hardcoded keyword detection with nuanced context‑aware classification.
- **Safety Guardrails**: Pre‑processing blocks spam/empty input; post‑processing adds appropriate disclaimers based on triage results.
- **Dual Interfaces**:
  - Terminal mode for quick testing (`src/main.py`).
  - Web UI with Chainlit (`src/web/app.py`).
- **Flexible LLM Backend**: Local (LMStudio, e.g., Qwen3‑4B) or OpenRouter (DeepSeek V3.2).
- **Pydantic‑AI Agent**: Structured tools/dependencies for reliable execution; main agent receives triage data for context‑aware responses.
- **Non‑blocking Emergency Handling**: Emergency alerts are shown but the conversation continues, ensuring usability while prioritizing safety.

## Architecture

```mermaid
graph TD
    A[User Input<br/>Terminal or Web UI] --> B[TriageAgent<br/>Classify: topic/lang/emergency/disclaimer]
    B -->|is_emergency=true| C[🚨 Emergency Alert<br/>Prepend Disclaimer]
    B -->|Safe| D[Basic Pre‑checks<br/>Empty/Spam/Length]
    D --> E[Main Agent<br/>w/ RAG Tool & triage_data]
    E --> F[Post‑process<br/>Add disclaimer if needed]
    F --> G[Final Response]
    style C fill:#ff9999
    style G fill:#99ff99
```

## Tech Stack

- **Core**: [Python 3.12+](https://www.python.org/), [`Pydantic‑AI`](src/agent.py) (agents/tools)
- **LLM**: OpenAI‑compatible (local via LMStudio/Ollama or OpenRouter)
- **UI**: [Chainlit](https://docs.chainlit.io/)
- **Database**: pgvector (mocked in [`src/database.py`](src/database.py))
- **Prompts/Guardrails**: [`src/prompts.py`](src/prompts.py) – now includes triage prompt and disclaimer config
- **Triage Module**: [`src/triage.py`](src/triage.py) – dedicated classification agent
- **Dependencies**: Managed via [uv](https://astral.sh/uv) + [`pyproject.toml`](pyproject.toml) (Torch, Transformers, HuggingFace, etc. for potential local models)
- **Package Manager**: uv (faster pip alternative)

## Quick Start

### Prerequisites
- [uv](https://astral.sh/uv) (recommended) or pip
- Local LLM (e.g., LMStudio with Qwen3‑4B) or OpenRouter API key

### Installation
1. Clone the repo:
   ```
   git clone https://gitlab.cmi.hro.nl/ncbj/rottermaatje.git
   cd rottermaatje
   ```
2. Install dependencies:
   ```
   uv sync  # or pip install -e .
   ```
3. Setup environment [`cp .env.example .env`](.env.example) and edit:
   ```
   MODEL_PROVIDER=local  # or openrouter
   OPENROUTER_API_KEY=sk-or-v1-...  # if using OpenRouter
   OPENAI_BASE_URL=http://localhost:1234/v1  # LMStudio default
   DATABASE_URL=postgresql://user:pass@localhost:5432/rottermaatje  # future
   ```

### Usage

#### Terminal Mode
```
python src/main.py
```
- Interactive chat: Type queries, `exit` to quit.
- Example: "Waar kan ik nachtopvang vinden?"
- The terminal shows triage classification (topic, language, emergency status) before each response.

#### Web UI (Chainlit)
```
uv run chainlit run src/web/app.py
```
- Open `http://localhost:8000`