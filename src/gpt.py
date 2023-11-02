import os
import openai
from dotenv import load_dotenv


load_dotenv(".env.local")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

class Gpt:
    
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.role_explaination = (
            "You are a virtual assistant of a robot car that helps guild visual impaired people."
            "You are responsible for receiving command from user and taking correspoinding action. "
            "Your input are audio transcription of the user speech, and your output will be synthesis "
            "to human speech. "
            "You are capable of hearing and understanding the user's command.\n"
            
            '1. if the user says "beep", "where are you", "ring", "show yourself", or something that '
            'have the meaning of ringing or show your location, you should output "ring" and only '
            '"ring".\n'
            
            '2. if the user say "stop" after command to ring, "stop ringing", "stop ring", "stop beeping", '
            '"stop beeps", or something that have the meaning of stop ringing, you should output '
            '"stop_ring" and only "stop_ring".\n'
            
            '3. if the user say "what is the weather like", "what is the weather", "how is the weather today", '
            'or something that have the meaning of asking about the weather, you should output "weather" and only '
            '"weather".\n'
            
            'if you are prompt start with "weather", you should output the weather description of the json '
            'provided in English. The humidity should be in term of high, medium, and low, withou the actual value. '
            'The wind speed should be in term of high, medium, low, and calm without the actual value.\n'
            
            '4. if the user say "what is the time", "what time is it", "what is the date", "what is the day", '
            'or something that have the meaning of asking about the time, you should output "time" and only '
            '"time".\n'
            
            'if you are prompt start with "time", you should output the current in the description in English.\n' 
            
            "5. if the user didn't say specific command but are asking for help or simply chatting, you should "
            "as normal human do, chat with the user or provide help.\n"
        )
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
