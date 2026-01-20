from spade_llm import LLMTool

from vulnagent.models.vlai import VLAISeverityClassifier


class SeverityClassifierTool:
    name = "severity_classifier"
    description = (
        "Classifies the severity of a vulnerability description "
        "using the VLAI RoBERTa-based model."
    )

    def __init__(self, model_name):
        self.classifier = VLAISeverityClassifier(model_name)

    def __call__(self, text):
        return self.classifier.classify(text)


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
                "description": "Vulnerability description to classify",
            }
        },
        "required": ["text"],
    },
    func=classify_severity,
)
