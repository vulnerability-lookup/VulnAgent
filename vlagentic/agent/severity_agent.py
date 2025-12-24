from spade_llm import LLMAgent, LLMTool

from vlagentic.tools.severity_classifier import SeverityClassifierTool
from vlagentic.agent.llm import get_llm_provider


# ---------------------------------------------------------------------------
# Tool definition (agentic-style)
# ---------------------------------------------------------------------------

_classifier = SeverityClassifierTool(
    model_name="CIRCL/vulnerability-severity-classification-roberta-base"
)

async def classify_severity(text: str) -> dict:
    """
    Tool wrapper used by the LLM.
    """
    return _classifier(text)


severity_tool = LLMTool(
    name="classify_severity",
    description=(
        "Classify the severity of a vulnerability description using "
        "the VLAI RoBERTa-based model. Returns severity label and confidence."
    ),
    parameters={
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Vulnerability description to classify"
            }
        },
        "required": ["text"]
    },
    func=classify_severity,
)


# ---------------------------------------------------------------------------
# Agent definition
# ---------------------------------------------------------------------------

class SeverityAgent(LLMAgent):
    def __init__(self, jid: str, password: str):
        super().__init__(
            jid=jid,
            password=password,
            provider=get_llm_provider(),
            system_prompt=(
                "You are a security analysis agent.\n\n"
                "You receive messages that may contain vulnerability descriptions.\n"
                "When appropriate, classify their severity using the available tools.\n"
                "Explain results clearly and concisely for a security audience.\n"
                "If classification is not relevant, respond directly."
            ),
            tools=[severity_tool],
        )
