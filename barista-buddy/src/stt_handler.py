import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class STTHandler:
    def __init__(self, model_path, samplerate=16000):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, samplerate)
        self.samplerate = samplerate

    def listen(self, duration=5):
        audio = sd.rec(int(duration * self.samplerate),
                        samplerate=self.samplerate,
                        channels=1,
                        dtype='int16')
        sd.wait()

        self.recognizer.AcceptWaveform(audio.tobytes())
        result = json.loads(self.recognizer.Result())
        return result.get("text", "")
