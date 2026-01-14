class LLMHandler:
    def generate(self, query, retrieved_answer=None):
        if retrieved_answer:
            return retrieved_answer
        return "I'm sorry, I can only help with coffee-related questions."
