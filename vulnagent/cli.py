import asyncio

from vulnagent.commands.run_all import main as async_main


def main():
    asyncio.run(async_main())
