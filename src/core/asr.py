import warnings
import os
import json
from abc import ABC, abstractmethod

import whisper
import openai
from dotenv import load_dotenv
# from vosk import Model, KaldiRecognizer
import vosk


from src.core.wav_file_writer import WavFileWriter

load_dotenv(".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

wav_file_writer = WavFileWriter()

class Asr(ABC):
    @abstractmethod
    def __call__(self, audio_file):
        pass

class Streaming(ABC):
    @abstractmethod
    def reset(self):
        pass

class WhisperLocal(Asr):
    def __init__(self, model_size="small"):
        self.model = whisper.load_model(model_size)

    def __call__(self, audio_bytes):
        audio_file_path = "./tmp.wav"
        wav_file_writer(audio_bytes, audio_file_path)
        return self.model.transcribe(audio_file_path)["text"]


class WhisperCloud(Asr):
    def __init__(self, model="whisper-1"):
        self.model = model

    def __call__(self, audio_bytes):
        audio_file_path = "./tmp.wav"
        wav_file_writer(audio_bytes, audio_file_path)
        with open(audio_file_path, "rb") as audio_file:
            return openai.Audio.transcribe(self.model, audio_file)["text"]


class Vosk(Asr, Streaming):
    def __init__(self, model_path="./models/vosk-model-en-us-0.22"):
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.result = ""

    def __call__(self, audio):
        if self.recognizer.AcceptWaveform(audio):
            self.result = json.loads(self.recognizer.Result())["text"]
        else:
            self.result =  json.loads(self.recognizer.PartialResult())["partial"]

    def reset(self):
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.result = ""
