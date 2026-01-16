# AI-Voice-Assistant-NLP-PROJECT: Barista Buddy


Barista Buddy is a **voice-only AI assistant** specialized in coffee knowledge. It can listen to your voice, answer coffee-related questions, and speak back to you. If it doesn’t know the answer from its FAQ, it falls back to a local language model (**DistilGPT-2**) with prompt engineering.

---
## 📊 Poster

Here’s the poster for the Barista Buddy project:

<p align="center">
  <img src="Barista Buddy.png" width="600">
</p>

## 🔹 Features

- 🎤 **Voice input (Speech-to-Text)**  
- 🤖 **Voice output (Text-to-Speech)**  
- ☕ **Coffee knowledge FAQ**  
- 💡 **Fallback to LLM (DistilGPT-2) for unknown coffee questions**  
- ❌ **Rejects non-coffee questions**  
- ⚡ **Continuous listening mode**

---

## 🔹 Project Overview

This project demonstrates a complete **voice assistant pipeline**:

1. **Speech-to-Text (STT)**  
   Converts spoken words to text using the `speech_recognition` library.

2. **Natural Language Processing (NLP) / LLM**  
   - FAQ retrieval first: searches a curated coffee knowledge base for exact or fuzzy matches.  
   - LLM fallback: uses **DistilGPT-2** with prompt engineering to generate coffee-focused responses if the FAQ doesn't match.

3. **Text-to-Speech (TTS)**  
   Converts the assistant's answer back to speech using `pyttsx3`.

4. **Domain Customisation**  
   Uses coffee-specific keywords, a pronunciation dictionary, and prompt engineering to ensure that responses stay coffee-focused.

---

## 🔹 Methodology
 **Architecture Diagram**

<p align="center">
  <img src="architecture diagram.png" alt="Barista Buddy Architecture" width="600">
</p>

*Figure 1: Barista Buddy system architecture showing STT, Fuzzy Matcher, Topic Filter, FAQ, LLM fallback, and TTS pipeline.*


**Detailed steps:**

1. **Listen**: Captures user speech via microphone.
2. **STT**: Converts speech to text.
3. **Fuzzy Matcher**: Corrects common mispronunciations.
4. **Topic Filter**: Ensures query is coffee-related.
5. **FAQ Retrieval**: Searches knowledge base for best match.
6. **LLM Query**: If no FAQ match, DistilGPT-2 generates response using a coffee-specific prompt.
7. **TTS Output**: Speaks the response back to the user.
8. **Continuous Listening**: Keeps listening for queries until a stop word is detected.

---

## 🔹 Results & Discussion

- **FAQ Matching**: Most common coffee questions are answered instantly from the knowledge base.  
- **LLM Fallback**: DistilGPT-2 produces coherent coffee-focused answers for unlisted queries.  
- **Speech Recognition Accuracy**: Fuzzy text correction improves recognition of coffee terminology.  
- **Limitations**: LLM may generate generic responses; non-coffee queries rely on keyword filtering which is not perfect.  
- **Potential Improvements**:  
  - Upgrade to more advanced LLMs (e.g., GPT-3.5 or GPT-4).  
  - Add wake word support.  
  - Dynamically expand the FAQ database based on user interactions.

---

## 🔹 Conclusion

Barista Buddy effectively demonstrates a **hybrid FAQ + LLM** AI assistant. It combines structured domain knowledge with generative AI to provide accurate, coffee-focused responses, making it a practical example of a domain-specific conversational AI.

---

## 🔹 References

1. Hugging Face Transformers: [https://huggingface.co/docs/transformers](https://huggingface.co/docs/transformers)  
2. Pyttsx3 TTS Library: [https://pyttsx3.readthedocs.io](https://pyttsx3.readthedocs.io)  
3. SpeechRecognition Library: [https://pypi.org/project/SpeechRecognition/](https://pypi.org/project/SpeechRecognition/)  
4. DistilGPT-2 Model Card: [https://huggingface.co/distilgpt2](https://huggingface.co/distilgpt2)  

---

## 🔹 Setup & Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/AI-Voice-Assistant-NLP-PROJECT.git
```
2. Make sure you have Python 3.9+ installed.

3. Install required packages:
 ```bash
pip install -r requirements.txt

```

