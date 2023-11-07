import os
import openai
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

class Gpt:

    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.role_explaination = Path("./assets/prompt.txt").read_text()
        self.history = []

    def __call__(self, command):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                { "role": "system", "content": self.role_explaination },
                *self.history,
                { "role": "user", "content": command },
            ]
        )
        response_content = completion['choices'][0]['message']['content']
        self.history.extend([
            { "role": "user", "content": command },
            { "role": "system", "content": response_content }
        ])
        return response_content
