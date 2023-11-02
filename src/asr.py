import warnings
import os
from abc import ABC, abstractmethod

import whisper
import openai
from dotenv import load_dotenv
# from vosk import Model, KaldiRecognizer
import vosk


load_dotenv(".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")


class Asr(ABC):
    @abstractmethod
    def __call__(self, audio_file):
        pass


class WhisperLocal(Asr):
    def __init__(self, model_size="small"):
        self.model = whisper.load_model(model_size)

    def __call__(self, audio_file):
        return self.model.transcribe(audio_file)["text"]


class WhisperCloud(Asr):
    def __init__(self, model="whisper-1"):
        self.model = model

    def __call__(self, audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            return openai.Audio.transcribe(self.model, audio_file)["text"]


class Vosk(Asr):
    def __init__(self, model_path="model"):
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

    def __call__(self, audio):
        if self.recognizer.AcceptWaveform(audio):
            print(self.recognizer.Result())
        else:
            print(self.recognizer.PartialResult())
