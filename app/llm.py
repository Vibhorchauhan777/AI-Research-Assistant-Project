from langchain_community.chat_models import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatOllama(
        model=os.getenv("MODEL_NAME", "qwen3:8b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0.3
    )