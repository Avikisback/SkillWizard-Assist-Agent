import os
from typing import Optional

from langchain_community.chat_models import ChatOllama


def get_llm() -> Optional[ChatOllama]:
    mode = os.getenv("SKILLWIZ_LLM", "ollama").lower()
    if mode == "none":
        return None
    if mode != "ollama":
        return None

    model = os.getenv("SKILLWIZ_OLLAMA_MODEL", "qwen2.5:7b")
    base_url = os.getenv("OLLAMA_BASE_URL")
    if base_url:
        return ChatOllama(model=model, base_url=base_url)
    return ChatOllama(model=model)
