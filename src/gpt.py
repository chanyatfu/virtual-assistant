import os
import openai
from dotenv import load_dotenv


load_dotenv(".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

class Gpt:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        
    def __call__(self, command):
        completion = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """
                        You are a virtual assistant in a robot car that helps guild visual impaired people.
                        You are responsible for receiving command from user and taking correspoinding action.
                        The Input language is English and the output language is English.
                    """
                },
                {
                    "role": "user",
                    "content": command
                },
            ]
        )
        return completion['choices'][0]['message']['content']
