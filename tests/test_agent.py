import asyncio

from spade.message import Message
from test_severity_agent import TestSeverityAgent


async def main():
    agent = TestSeverityAgent("test_agent@localhost", "password")
    await agent.start()
    print("TestSeverityAgent running...")

    # Send a test message to self
    msg = Message(to="test_agent@localhost")
    msg.body = "The application has a buffer overflow in the authentication module."
    await agent.send(msg)

    # Give some time to process
    await asyncio.sleep(5)

    await agent.stop()


asyncio.run(main())
