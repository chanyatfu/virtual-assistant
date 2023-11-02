import warnings
import os

import whisper
import openai
from dotenv import load_dotenv


load_dotenv(".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

class WhisperLocal:
    def __init__(self, model_size="small"):
        self.model = whisper.load_model(model_size)

    def __call__(self, audio_file):
        return self.model.transcribe(audio_file)["text"]

class WhisperCloud:
    def __init__(self, model="whisper-1"):
        self.model = model

    def __call__(self, audio_file_path):
        with open(audio_file_path, "rb") as audio_file:
            return openai.Audio.transcribe(self.model, audio_file)["text"]
