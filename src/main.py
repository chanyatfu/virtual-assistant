from src.core.recorder import Recorder
from src.core.asr import WhisperCloud, Asr, Vosk, WhisperLocal
from src.core.gpt import Gpt
from src.core.tts import Tts
from src.core.audio_player import AudioPlayer
from src.helpers.clear_line import clear_line
from src.plugin import clock, weather, expose


class Assistant:
    def __init__(self):
        self.recorder = Recorder()
        self.asr: Asr = Vosk()
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
                input = self.asr.result
                self.asr.reset()
                print(clear_line + "You said: " + input)
                output = self.gpt(input)
                self.handle_answer(output)

    
    def handle_answer(self, answer): 
        match (answer):
            case "ring":
                expose.start()
            case "stop_ring":
                expose.stop()
            case "weather":
                self.player.load_and_play_once("./assets/received.wav")
                ret = weather.get_weather()
                print(ret)
                output = self.gpt("weather\n" + ret)
                print(clear_line + "Assistant said: " + output)
                self.tts(output)
            case "time":
                self.player.load_and_play_once("./assets/received.wav")
                time = clock.get_time()
                output = self.gpt("time\n" + time)
                print(clear_line + "Assistant said: " + output)
                self.tts(output)
            case "none":
                pass
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
