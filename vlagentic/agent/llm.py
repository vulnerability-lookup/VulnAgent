from spade_llm import LLMProvider


def get_llm_provider():
    """
    Returns an LLMProvider configured for Ollama.
    """
    return LLMProvider.create_ollama(
        model="llama3.1:8b",
        base_url="http://localhost:11434/v1"
    )
