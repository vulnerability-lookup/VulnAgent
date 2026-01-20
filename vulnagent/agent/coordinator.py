from spade_llm.agent import CoordinatorAgent
from spade.message import Message
from vulnagent.agent.llm import get_llm_provider


def routing_function(msg, response, context):
    """
    Pure routing function.
    Decide which subagent should receive the message.
    """
    text = msg.body.lower()

    if any(k in text for k in ["severity", "cwe", "vulnerability"]):
        return "vlai_assistant@localhost"

    if any(op in text for op in ["+", "-", "*", "/", "calculate"]):
        return "tool_assistant@localhost"

    return "tool_assistant@localhost"


def init_coordinator_agent(domain: str):
    """
    Initialize a CoordinatorAgent with routing to two specialized LLM agents.
    """
    coordinator = CoordinatorAgent(
        jid=f"coordinator@{domain}",
        password="password",
        subagent_ids=[
            f"vlai_assistant@{domain}",
            f"tool_assistant@{domain}",
        ],
        provider=get_llm_provider(),
        routing_function=routing_function,
        coordination_session="session",
    )
    return coordinator
