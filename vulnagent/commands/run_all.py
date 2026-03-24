import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from vulnagent.agent.chat import init_chat_agent
from vulnagent.agent.llm import init_llm_agent, tools
from vulnagent.config import get_config


class AutoAcceptPresence(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if not msg:
            return

        if msg.metadata.get("performative") == "subscribe":
            jid = str(msg.sender)
            print(f"🔔 Accepting presence subscription from {jid}")
            self.agent.presence.approve(jid)
        else:
            await self.agent.queue.put(msg)


class WebUIBridge(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=1)
        if not msg:
            return

        sender_jid = str(msg.sender).split("/")[0]
        my_jid = str(self.agent.jid).split("/")[0]

        # 1. IGNORE messages I sent to myself (the LLM processing loop)
        if sender_jid == my_jid:
            return

        # 2. If it's a message from the USER, handle it
        print(f"🌉 Bridge received from {sender_jid}: {msg.body}")

        # We don't necessarily need to "forward" it to self.agent.jid
        # if the LLMAgent is already listening.
        # If you WANT to manually trigger the LLM, use a specific metadata:

        llm_msg = Message(to=str(self.agent.jid))
        llm_msg.body = msg.body
        llm_msg.set_metadata("performative", "inform")
        llm_msg.set_metadata("is_bridge_forward", "true")  # Mark it!

        # Note: If LLMAgent is already running its default behaviour,
        # it will catch the message from the USER directly.
        # You might be double-triggering it.


async def main():
    cfg = get_config()
    default_server = cfg["xmpp"]["server"]
    xmpp_server = input(f"XMPP server domain (default: {default_server}): ") or default_server

    llm_agent = init_llm_agent(xmpp_server)
    chat_agent = init_chat_agent(xmpp_server)

    # Add behaviours
    # llm_agent.add_behaviour(WebUIBridge())
    # llm_agent.add_behaviour(AutoAcceptPresence())

    try:
        await llm_agent.start()
        await chat_agent.start()

        llm_agent.presence.set_available()
        chat_agent.presence.set_available()

        llm_agent.presence.on_subscribe = lambda jid: llm_agent.presence.approve(jid)
        chat_agent.presence.on_subscribe = lambda jid: chat_agent.presence.approve(jid)

        # Mutual subscription
        chat_agent.presence.subscribe(f"tool_assistant@{xmpp_server}")
        llm_agent.presence.subscribe(f"user@{xmpp_server}")

        print("✅ Agents started!")
        print("🔧 Available tools:")
        for tool in tools:
            print(f"• {tool.name}")
        print("\n💡 Try these queries:")
        print("• 'What's the severity of the vulnerability described by ...?'")
        print("• 'What time is it?'")
        print("• 'Calculate 15 * 8 + 32'")
        print("• 'What's the weather in Luxembourg?'")

        # Start agents web interfaces
        await llm_agent.web.start(hostname="127.0.0.1", port="10000")
        print("LLM Agent Web Interface: http://127.0.0.1:10000/spade")
        await chat_agent.web.start(hostname="127.0.0.1", port="10001")
        print("Chat Agent Web Interface: http://127.0.0.1:10001/spade")

        # Run interactive chat
        await chat_agent.run_interactive(response_timeout=300)
        # # Keep agents alive
        # while True:
        #     await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        await chat_agent.stop()
        await llm_agent.stop()
        print("✅ Agents stopped successfully!")


if __name__ == "__main__":
    print("🚀 Prerequisites:")
    print("• Ollama running: ollama serve")
    print("• Model available: ollama pull qwen2.5:7b")
    print("• XMPP server running")
    print()
    spade.run(main())
