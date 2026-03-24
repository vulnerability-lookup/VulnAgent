from spade_llm.agent import CoordinatorAgent
from spade.message import Message
from vulnagent.agent.llm import get_llm_provider
from vulnagent.config import get_config


def routing_function(msg, response, context):
    """
    Pure routing function.
    Decide which subagent should receive the message.
    """
    cfg = get_config()
    domain = cfg["xmpp"]["server"]
    vlai_jid = f"{cfg['agents']['vlai']['name']}@{domain}"
    llm_jid = f"{cfg['agents']['llm']['name']}@{domain}"

    text = msg.body.lower()

    if any(k in text for k in ["severity", "cwe", "vulnerability"]):
        return vlai_jid

    if any(op in text for op in ["+", "-", "*", "/", "calculate"]):
        return llm_jid

    return llm_jid


def init_coordinator_agent(domain: str):
    """
    Initialize a CoordinatorAgent with routing to two specialized LLM agents.
    """
    cfg = get_config()
    agent_cfg = cfg["agents"]["coordinator"]

    coordinator = CoordinatorAgent(
        jid=f"{agent_cfg['name']}@{domain}",
        password=agent_cfg["password"],
        subagent_ids=[
            f"{cfg['agents']['vlai']['name']}@{domain}",
            f"{cfg['agents']['llm']['name']}@{domain}",
        ],
        provider=get_llm_provider(),
        routing_function=routing_function,
        coordination_session="session",
    )
    return coordinator
