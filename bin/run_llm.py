import asyncio

from scripts.run_llm import main as async_main


def main():
    asyncio.run(async_main())
