from datetime import datetime

from spade_llm import LLMTool


def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


current_time_tool = LLMTool(
    name="get_current_time",
    description="Get the current date and time",
    parameters={"type": "object", "properties": {}, "required": []},
    func=get_current_time,
)
