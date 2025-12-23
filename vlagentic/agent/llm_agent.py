import asyncio

import spade
from spade_llm import LLMAgent, LLMProvider


async def main():
    # OpenAI
    # provider = LLMProvider.create_openai(
    #     api_key="your-api-key",
    #     model="gpt-4o-mini"
    # )
    # or use a local model:
    provider = LLMProvider.create_ollama(model="llama3.1:8b")

    agent = LLMAgent(
        jid="assistant@localhost",  # Connects to built-in server
        password="password",
        provider=provider,
        system_prompt="You are a helpful vulnerability assistant powered by VLAI."
    )

    await agent.start()

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
