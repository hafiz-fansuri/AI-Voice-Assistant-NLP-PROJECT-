from difflib import get_close_matches
import json

class FuzzyMatcher:
    def __init__(self, pronunciation_file):
        with open(pronunciation_file, "r") as f:
            self.pronunciations = json.load(f)

    def normalize(self, text):
        for correct, variants in self.pronunciations.items():
            if text in variants:
                return correct
        return text

    def fuzzy_match(self, text):
        keys = list(self.pronunciations.keys())
        match = get_close_matches(text, keys, n=1, cutoff=0.7)
        return match[0] if match else text
