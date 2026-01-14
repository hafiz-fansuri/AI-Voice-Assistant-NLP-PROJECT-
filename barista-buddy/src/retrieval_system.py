import json
from difflib import SequenceMatcher

class RetrievalSystem:
    def __init__(self, knowledge_file):
        with open(knowledge_file, "r") as f:
            self.knowledge = json.load(f)

    def similarity(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def retrieve(self, query):
        best_score = 0
        best_answer = None

        for item in self.knowledge:
            score = self.similarity(query.lower(), item["question"].lower())
            if score > best_score:
                best_score = score
                best_answer = item["answer"]

        return best_answer if best_score > 0.5 else None
