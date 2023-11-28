from src.core.recorder import Recorder
from src.core.asr import WhisperCloud, Asr, Vosk, WhisperLocal
from src.core.gpt import Gpt
from src.core.tts import Tts
from src.core.audio_player import AudioPlayer
from src.helpers.clear_line import clear_line
from src.plugin import clock, weather, expose
import requests
from dotenv import load_dotenv
import os
import re

load_dotenv(".env.local")
jetson_nano_ip = os.getenv("JETSON_NANO_IP")

class Assistant:
    def __init__(self):
        self.recorder = Recorder()
        self.asr: Asr = WhisperCloud()
        self.gpt = Gpt()
        self.tts = Tts()
        self.player = AudioPlayer()
        self.recorder.init()

    def run(self):
        while True:
            byte = self.recorder.iter()
            if (byte):
                self.asr(byte)
            if (self.recorder.finished):
                input = self.asr.fetch()
                self.asr.reset()
                input = re.sub("[^\w ]", '',input.lower())
                print(clear_line + "You said: " + input)
                match (input):
                    case "move forward" | "forward" | "go forward" | "go ahead" | "go" | "advance" | "release" | "move" | "ahead":
                        requests.get(f"http://{jetson_nano_ip}/test/A")
                    case "stop it" | "stop the car" | "africa" | "replica" | "stop moving" | "stop" | "not moving" | "stationary" | "stay" | "down" | "stationery" | "its not moving" | "start moving":
                        requests.get(f"http://{jetson_nano_ip}/test/Z")
                    case "go backward" | "go back" | "go backwards" | "backward" | "back" | "move backward" | "move back" | "move backwards":
                        requests.get(f"http://{jetson_nano_ip}/test/E")
                    case "go left" | "left" | "go to the left" | "to the right":
                        requests.get(f"http://{jetson_nano_ip}/test/H")
                    case "go right" | "right" | "go to the right" | "to the right":
                        requests.get(f"http://{jetson_nano_ip}/test/B")
                    case "where are you":
                        requests.get(f"http://{jetson_nano_ip}/test/P")
                    case "stop ringing" | "i found you" | "stop raining":
                        requests.get(f"http://{jetson_nano_ip}/test/Q")
                    case "summarize" | "summer ice" | "in front of you" | "what is in front of you" | "is in front of you":
                        requests.get(f"http://{jetson_nano_ip}/test/K")
                    case "how is the weather today" | "its still wetter today":
                        requests.get(f"http://{jetson_nano_ip}/test/R")
                    case "what time is it":
                        requests.get(f"http://{jetson_nano_ip}/test/T")
                    case "spin around" | "turn around" | "turn her on" | "turner on":
                        requests.get(f"http://{jetson_nano_ip}/test/C")
                    case "tracking" | "tracing" | "follow the line":
                        requests.get(f"http://{jetson_nano_ip}/test/U")
                    # case _:
                    #     output = self.gpt(input)
                    #     self.handle_answer(output)

    def handle_answer(self, answer):
        match (answer):
            case "ring":
                requests.get(f"http://{jetson_nano_ip}/test/P")
            case "stop_ring":
                requests.get(f"http://{jetson_nano_ip}/test/Q")
            case "weather":
                self.player.load_and_play_once("./assets/received.wav")
                weather_info = weather.get_weather()
                print("weather info" + weather_info)
                output = self.gpt("Describe {weather} in English." + weather_info)
                print(clear_line + "Assistant said: " + output)
                self.tts(output)
            case "time":
                self.player.load_and_play_once("./assets/received.wav")
                time = clock.get_time()
                output = self.gpt("Describe {time} in English." + time)
                print(clear_line + "Assistant said: " + output)
                self.tts(output)
            case "none":
                pass
            case "forward":
                requests.get(f"http://{jetson_nano_ip}/test/A")
            case "backward":
                requests.get(f"http://{jetson_nano_ip}/test/E")
            case "stop":
                requests.get(f"http://{jetson_nano_ip}/test/Z")
            case _:
                self.player.load_and_play_once("./assets/received.wav")
                print(clear_line + "Assistant said: " + answer)
                self.tts(answer)

    def terminate(self):
        self.recorder.terminate()
        self.player.stop()


def main():
    assistant = Assistant()
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        assistant.terminate()


if __name__ == '__main__':
    main()

