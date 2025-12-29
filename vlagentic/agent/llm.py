import getpass

from spade_llm import LLMAgent, LLMProvider

from vlagentic.tools.current_time import current_time_tool
from vlagentic.tools.math import math_tool
from vlagentic.tools.severity import severity_tool
from vlagentic.tools.weather import weather_tool


def get_llm_provider(model="qwen2.5:7b", temperature=0.7):
    """
    Returns an LLMProvider configured for Ollama.
    (qwen2.5:7b, llama3.1:8b)
    """
    return LLMProvider.create_ollama(
        model=model, base_url="http://localhost:11434/v1", temperature=temperature
    )


tools = [
    severity_tool,
    weather_tool,
    current_time_tool,
    math_tool,
]


def init_llm_agent(xmpp_server):
    llm_agent = LLMAgent(
        jid=f"tool_assistant@{xmpp_server}",
        password=getpass.getpass("LLM agent password: "),
        provider=get_llm_provider(),
        system_prompt=(
            "You are a helpful assistant with access to tools: classify_severity, get_current_time, calculate_math, and get_weather. "
            "Use these tools when appropriate to help users. "
            "You receive messages that may contain vulnerability descriptions.\n"
            "When appropriate, classify their severity using the available tools.\n"
            "Explain results clearly and concisely for a security audience.\n"
            "If classification is not relevant, respond directly."
        ),
        tools=tools,
    )
    return llm_agent
