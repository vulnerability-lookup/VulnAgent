import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

from vlagentic.tools.severity_classifier import SeverityClassifierTool


class SeverityAgent(Agent):
    async def setup(self):
        self.tool = SeverityClassifierTool(
            model_name="CIRCL/vulnerability-severity-classification-roberta-base"
        )
        self.add_behaviour(self.ClassifyBehaviour())

    class ClassifyBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if not msg:
                return

            text = msg.body
            result = self.agent.tool(text)

            reply = Message(to=msg.sender)
            reply.body = str(result)
            await self.send(reply)
