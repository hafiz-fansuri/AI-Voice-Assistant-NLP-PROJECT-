class TopicFilter:
    def __init__(self, keyword_file):
        with open(keyword_file, "r") as f:
            self.keywords = [k.strip() for k in f.readlines()]

    def is_coffee_related(self, text):
        text = text.lower()
        return any(keyword in text for keyword in self.keywords)
