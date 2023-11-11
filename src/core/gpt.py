import os
import openai
from dotenv import load_dotenv
from pathlib import Path
from typing import cast, Any

load_dotenv(".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

class Gpt:
    def __init__(self, model=os.getenv("GPT_MODEL_ID")):
        self.model = model
        self.role_explaination = Path("./assets/prompt.txt").read_text()
        self.history = []

    def __call__(self, command):
        completion = cast(dict[str, Any], openai.ChatCompletion.create(
            model=self.model,
            messages=[
                { "role": "system", "content": self.role_explaination },
                *self.history,
                { "role": "user", "content": command },
            ]
        ))
        response_content = completion['choices'][0]['message']['content']
        self.history.extend([
            { "role": "user", "content": command },
            { "role": "system", "content": response_content }
        ])
        return response_content
