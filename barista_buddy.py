"""
Barista Buddy - Voice-Only AI Voice Assistant with LLM fallback
- Voice input & output
- Rejects non-coffee questions
- Fallback to LLM if coffee question not in FAQ
"""

import json
from pathlib import Path
import difflib
import pyttsx3
import speech_recognition as sr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ---------------------------
# STT HANDLER
# ---------------------------
class STTHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self, timeout=5, phrase_time_limit=4) -> str:
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            print("🎤 Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                return self.recognizer.recognize_google(audio).lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return ""

# ---------------------------
# TTS HANDLER
# ---------------------------
class TTSHandler:
    def __init__(self, rate=180):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text):
        print(f"\n🤖 Barista Buddy: {text}\n")
        self.engine.say(text)
        self.engine.runAndWait()

# ---------------------------
# FUZZY MATCHER
# ---------------------------
class FuzzyMatcher:
    def __init__(self, pronunciation_dict):
        self.pronunciation_dict = pronunciation_dict

    def correct_text(self, text: str) -> str:
        text = text.lower()
        for wrong, correct in self.pronunciation_dict.items():
            if isinstance(correct, list):
                correct = correct[0]
            if isinstance(correct, str):
                text = text.replace(wrong.lower(), correct.lower())
        return text

# ---------------------------
# TOPIC FILTER
# ---------------------------
class TopicFilter:
    def __init__(self, keywords):
        self.keywords = keywords

    def is_coffee_related(self, text: str) -> bool:
        return any(kw in text.lower() for kw in self.keywords)

# ---------------------------
# RETRIEVAL SYSTEM
# ---------------------------
class RetrievalSystem:
    def __init__(self, knowledge_list, cutoff=0.6):
        self.knowledge_dict = {}
        self.cutoff = cutoff
        for item in knowledge_list:
            question = item.get("question", "").lower()
            answer = item.get("answer", "")
            if question and answer:
                self.knowledge_dict[question] = answer

    def retrieve(self, query, top_k=3):
        query = query.lower()
        keys = list(self.knowledge_dict.keys())
        matches = difflib.get_close_matches(query, keys, n=top_k, cutoff=self.cutoff)
        return [{"question": k, "answer": self.knowledge_dict[k]} for k in matches]

# ---------------------------
# LLM HANDLER
# ---------------------------
class LLMHandler:
    def __init__(self, model_name="distilgpt2"):
        print("Loading LLM model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        print("LLM ready!")

    def query(self, text: str) -> str:
        prompt = (
            "You are Barista Buddy, a coffee-only assistant. "
            "Only answer questions related to coffee. "
            "If the question is not about coffee, say: 'Sorry, I can only answer coffee questions.'\n\n"
            f"User: {text}\nBarista Buddy:"
        )
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            inputs, 
            max_length=200,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Only take the assistant part
        return response.split("Barista Buddy:")[-1].strip()

# ---------------------------
# BARISTA BUDDY MAIN APP
# ---------------------------
class BaristaBuddy:
    def __init__(self, data_dir):
        print("\n☕ BARISTA BUDDY (VOICE ONLY with LLM fallback)")
        print("=" * 60)

        base_dir = Path(data_dir)

        # Load datasets
        with open(base_dir / "coffee_keywords.txt", encoding="utf-8") as f:
            keywords = [l.strip().lower() for l in f if l.strip()]

        with open(base_dir / "coffee_knowledge.json", encoding="utf-8") as f:
            knowledge_list = json.load(f)

        with open(base_dir / "pronunciation_dict.json", encoding="utf-8") as f:
            pronunciation = json.load(f)

        # Initialize components
        self.stt = STTHandler()
        self.tts = TTSHandler(rate=180)
        self.fuzzy_matcher = FuzzyMatcher(pronunciation)
        self.topic_filter = TopicFilter(keywords)
        self.retrieval = RetrievalSystem(knowledge_list, cutoff=0.5)
        self.llm = LLMHandler(model_name="distilgpt2")

        print("✓ Voice input enabled")
        print("✓ Voice output enabled")
        print("✓ LLM fallback enabled")
        print("=" * 60 + "\n")

    # ---------------------------
    # PROCESS QUERY
    # ---------------------------
    def process_query(self, query: str) -> str:
        query = self.fuzzy_matcher.correct_text(query)
        print(f"📝 Normalized query: {query}")

        # Step 1: Topic filter
        if not self.topic_filter.is_coffee_related(query):
            return "Sorry, I can only help with coffee-related questions."

        # Step 2: FAQ retrieval
        results = self.retrieval.retrieve(query)
        if results:
            return results[0]["answer"]

        # Step 3: LLM fallback for coffee-related questions
        return self.llm.query(query)

    # ---------------------------
    # RUN LOOP
    # ---------------------------
    def run(self):
        self.tts.speak("Hello! I'm Barista Buddy. How can I help you?")

        while True:
            try:
                query = self.stt.listen(timeout=5, phrase_time_limit=4)
                if not query.strip():
                    self.tts.speak("I didn't catch that. Please say it again.")
                    continue

                if query.lower() in ["exit", "quit", "goodbye"]:
                    self.tts.speak("Goodbye! Happy brewing!")
                    break

                answer = self.process_query(query)
                self.tts.speak(answer)

            except KeyboardInterrupt:
                self.tts.speak("Exiting Barista Buddy. Goodbye!")
                break

# ---------------------------
# ENTRY POINT
# ---------------------------
def main():
    data_folder = r"C:\Users\fansuri\Documents\pro\barista-buddy\DATA FILES"
    app = BaristaBuddy(data_dir=data_folder)
    app.run()

if __name__ == "__main__":
    main()
