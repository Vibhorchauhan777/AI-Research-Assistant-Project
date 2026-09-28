# 🧠 AI Research Assistant

A powerful, open-source AI Research Agent that performs multi-source web research, analyzes information, and synthesizes structured answers using local Language Models. Built on top of **LangGraph**, **LangChain**, and **Streamlit**.

## ✨ Features

- **Multi-Source Retrieval:** Integrates seamlessly with Tavily for high-quality, up-to-date web searches.
- **Local LLM Support:** Fully compatible with local, privacy-preserving LLMs via **Ollama** (defaults to `qwen3:8b`).
- **Structured Reasoning:** Powered by LangGraph for robust, node-based agent orchestration and execution traces.
- **Beautiful UI:** A clean, intuitive Streamlit interface that shows the agent's thought process, formatted answers, and cited source links.
- **Extensible Architecture:** Easily swap out models, vector stores (supports ChromaDB & Faiss), or add new search tools.

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) (For running local LLMs)
- A [Tavily API Key](https://tavily.com/)

### 2. Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/AI-Research-Assistant-Project.git
cd AI-Research-Assistant-Project-main

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory (or modify the existing one) with the following parameters:

```ini
APP_NAME=AI Research Assistant
DEBUG=true

# Get your API key from tavily.com
TAVILY_API_KEY=your_tavily_api_key_here

# Local Ollama configuration
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=qwen3:8b
```

### 4. Pull the Local Model

Before running the application, make sure Ollama is running and you have downloaded your target model:

```bash
ollama run qwen3:8b
```

### 5. Run the Application

Start the Streamlit user interface:

```bash
streamlit run ui.py
```

The app will become available in your browser at `http://localhost:8501`.

---

## 🧪 Testing

The project includes built-in test scripts to verify individual components before launching the full UI:

- **`test_config.py`**: Verifies environment variable loading.
- **`test_llm.py`**: Verifies your connection to the local Ollama LLM.
- **`test_search.py`**: Verifies the Tavily web search integration.

Run any test using standard Python:
```bash
python test_llm.py
```

## 🛠️ Tech Stack

- **UI Framework:** [Streamlit](https://streamlit.io/)
- **Agent Orchestration:** [LangGraph](https://python.langchain.com/v0.1/docs/langgraph/) & [LangChain](https://www.langchain.com/)
- **Search Engine:** [Tavily](https://tavily.com/)
- **Local Inference:** [Ollama](https://ollama.com/)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

## 📝 License

This project is licensed under the MIT License.
