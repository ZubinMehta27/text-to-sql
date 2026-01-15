from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from text_to_sql_agent.config import settings


def get_llm():
    """
    Factory that returns a LangChain ChatModel
    based on configuration.
    """
    if settings.llm_provider == "ollama":
        return ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0.0,
        )

    if settings.llm_provider == "openai":
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.0,
        )

    # This should never happen because config validates it
    raise RuntimeError(f"Unsupported LLM provider: {settings.llm_provider}")
