import asyncio

from scripts.run_chat import main as async_main


def main():
    asyncio.run(async_main())
