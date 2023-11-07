import os
from dotenv import load_dotenv
from elevenlabs import generate, play
from typing import cast

load_dotenv(".env.local")

eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")

class Tts:
    def __init__(self):
        pass

    def __call__(self, text):
        audio = generate(text=text, voice="Dorothy", model="eleven_multilingual_v2", api_key=eleven_labs_api_key)
        audio = cast(bytes, audio)
        play(audio)
