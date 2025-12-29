import getpass

from spade_llm import ChatAgent


def display_response(message: str, sender: str):
    print(f"\n🤖 Tool Assistant: {message}")
    print("-" * 50)


def init_chat_agent(xmpp_server):
    chat_agent = ChatAgent(
        jid=f"user@{xmpp_server}",
        password=getpass.getpass("Chat agent password: "),
        target_agent_jid=f"tool_assistant@{xmpp_server}",
        display_callback=display_response,
    )
    return chat_agent
