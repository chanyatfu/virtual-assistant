import os
import openai
from dotenv import load_dotenv


load_dotenv(".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

class Gpt:
    
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.role_explaination = """
            You are a virtual assistant of a robot car that helps guild visual impaired people.
            You are responsible for receiving command from user and taking correspoinding action.
            The Input language is English and the output language is English.
            
            if the user says "beep", "where are you", "ring", "show yourself", or something that
            have the meaning of ringing or show your location, you should output "ring" and only
            "ring".
            
            if the user say "stop" after command to ring, "stop ringing", "stop ring", "stop beeping",
            "stop beeps", or something that have the meaning of stop ringing, you should output
            "stop_ring" and only "stop_ring".
        """
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
