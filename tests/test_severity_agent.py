from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from vulnagent.tools.severity_classifier import SeverityClassifierTool


class TestSeverityAgent(Agent):
    async def setup(self):
        self.classifier = SeverityClassifierTool(
            model_name="CIRCL/vulnerability-severity-classification-roberta-base"
        )
        self.add_behaviour(self.ClassifyBehaviour())

    class ClassifyBehaviour(CyclicBehaviour):
        async def run(self):
            # Wait for incoming messages
            msg = await self.receive(timeout=10)
            if not msg:
                return

            text = msg.body
            result = self.agent.classifier(text)

            reply = Message(to=msg.sender)
            reply.body = f"Classification result: {result}"
            await self.send(reply)
