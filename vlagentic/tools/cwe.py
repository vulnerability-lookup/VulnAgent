from spade_llm import LLMTool

from vlagentic.models.cwe import VLAICWEClassifier


class CWEClassifierTool:
    name = "cwe_classifier"
    description = (
        "Classifies a vulnerability description into CWE categories "
        "and maps them to parent CWEs using the VLAI model."
    )

    def __init__(
        self,
        model_name: str,
        mapping_path: str,
        top_k: int = 5,
    ):
        self.classifier = VLAICWEClassifier(
            model_name=model_name,
            mapping_path=mapping_path,
            top_k=top_k,
        )

    def __call__(self, text: str) -> dict:
        return self.classifier.predict_cwe(text)


_classifier = CWEClassifierTool(
    model_name="CIRCL/cwe-parent-vulnerability-classification-roberta-base",
    mapping_path="data/child_to_parent_mapping.json",
    top_k=5,
)


async def classify_cwe(text: str) -> dict:
    """
    Tool wrapper used by the LLM.
    """
    return _classifier(text)


cwe_tool = LLMTool(
    name="classify_cwe",
    description=(
        "Classify a vulnerability description into CWE categories. "
        "Returns the primary CWE, normalized confidence, and top CWE predictions."
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
    func=classify_cwe,
)
