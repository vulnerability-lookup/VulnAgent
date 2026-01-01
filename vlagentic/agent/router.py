from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from spade_llm import LLMAgent

from vlagentic.agent.llm import get_llm_provider


class RouterBehaviour(CyclicBehaviour):
    def __init__(self, subagents):
        super().__init__()
        self.subagents = subagents  # dict of LLMAgent instances

    async def run(self):
        msg = await self.receive(timeout=1)
        if not msg:
            return

        text = msg.body.lower()
        original_sender = str(msg.sender)
        print(f"[Router] Received: {text} from {original_sender}")

        # Determine target subagent
        if any(k in text for k in ["severity", "cwe", "vulnerability"]):
            target_agent = self.subagents["vlai_assistant"]
        else:
            target_agent = self.subagents["tool_assistant"]

        # Proper call to LLMAgent
        response = await target_agent.send_message_to_llm(msg.body)

        # Send response back to ChatAgent
        reply = Message(to=original_sender)
        reply.body = response
        await self.send(reply)
        print(f"[Router] Sent response to {original_sender}: {response}")


class RouterAgent(Agent):
    def __init__(self, jid, password, subagents):
        super().__init__(jid, password)
        self.subagents = subagents

    async def setup(self):
        b = RouterBehaviour(self.subagents)
        self.add_behaviour(b)


def init_router_agent(subagents):
    router_agent = LLMAgent(
        jid="router@localhost",
        password="password",
        provider=get_llm_provider(),
        routing_function=smart_router,  # Dynamic routing
    )
    return router_agent
