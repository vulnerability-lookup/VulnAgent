import json
from transformers import pipeline


class VLAICWEClassifier:
    def __init__(
        self,
        model_name="CIRCL/cwe-parent-vulnerability-classification-roberta-base",
        mapping_path="data/child_to_parent_mapping.json",
        top_k=5,
    ):
        self.model_name = model_name
        self.top_k = top_k

        self.classifier = pipeline(
            task="text-classification",
            model=model_name,
            top_k=None,
        )

        with open(mapping_path, "r") as f:
            self.child_to_parent = json.load(f)

    def predict_cwe(self, text: str):
        results = self.classifier(text)[0]
        sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

        top_items = sorted_results[: self.top_k]

        mapped_results = {}
        scores = []

        for item in top_items:
            score = float(item["score"])
            scores.append(score)

            child_cwe = item["label"].replace("CWE-", "")
            parent_cwe = self.child_to_parent.get(child_cwe, child_cwe)
            mapped_results[f"CWE-{parent_cwe}"] = round(score, 4)

        normalized_confidence = scores[0] - scores[1] if len(scores) > 1 else scores[0]

        return {
            "agent": "cwe",
            "primary": list(mapped_results.keys())[0],
            "confidence": round(normalized_confidence, 4),
            "predictions": mapped_results,
            "model": self.model_name,
        }


if __name__ == "__main__":
    classifier = VLAICWEClassifier()

    result = classifier.predict_cwe("Fix buffer overflow in authentication handler")

    print(result)
