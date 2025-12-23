from vlagentic.models.vlai import VLAISeverityClassifier


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
