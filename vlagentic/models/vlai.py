import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class VLAISeverityClassifier:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()

    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)[0]

        idx = torch.argmax(probs).item()
        score = probs[idx].item()
        label = self.model.config.id2label[idx]

        return {
            "label": label,
            "confidence": round(score, 4),
            "model": self.model_name,
        }
