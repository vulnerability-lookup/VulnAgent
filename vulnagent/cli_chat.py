import asyncio

from vulnagent.commands.run_chat import main as async_main


def main():
    asyncio.run(async_main())
