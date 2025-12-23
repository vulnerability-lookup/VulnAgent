import asyncio

import spade

from vlagentic.agent.severity_agent import SeverityAgent


async def main():
    agent = SeverityAgent(
        "severity_agent@localhost",
        "password"
    )
    await agent.start()
    print("VLAgentIc running")

    # await asyncio.sleep(60)
    await agent.web.start(hostname="127.0.0.1", port="10000")
    print("Web Graphical Interface available at:")
    print("  http://127.0.0.1:10000/spade")
    print("Wait until user interrupts with ctrl+C")

    while True:  # not agent.CollectingBehav.is_killed():
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            break

    assert agent.CollectingBehav.exit_code == 10

    await agent.stop()


if __name__ == "__main__":
    spade.run(main())
