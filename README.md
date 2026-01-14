# AI-Voice-Assistant-NLP-PROJECT-
# Barista Buddy - Voice-Only AI Voice Assistant

**Barista Buddy** is a voice-based AI assistant specialised in coffee knowledge. It can listen to your voice, answer coffee-related questions, and speak back to you. If it doesn't know the answer from its FAQ, it can fall back to a local language model (DistilGPT-2) with prompt engineering.

---

## **Features**
- 🎤 Voice input (Speech-to-Text)  
- 🤖 Voice output (Text-to-Speech)  
- ☕ Coffee knowledge FAQ  
- 💡 Fallback to LLM (DistilGPT-2) for unknown coffee questions  
- ❌ Rejects non-coffee questions  

---

## **Project Overview**
This project demonstrates a complete voice assistant pipeline:
1. **Speech-to-Text (STT):** Converts spoken words to text using `speech_recognition`.  
2. **Natural Language Processing (NLP) / LLM:** Processes queries using DistilGPT-2 and prompt engineering.  
3. **Text-to-Speech (TTS):** Responds back to the user with speech using `pyttsx3`.  
4. **Domain Customisation:** Uses a coffee-specific FAQ and prompt engineering to ensure coffee-only answers.

---

## **Setup & Installation**
1. Clone the repository or download the files.  
2. Make sure you have Python 3.9+ installed.  
3. Install required packages:

```bash
pip install -r requirements.txt
