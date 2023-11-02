from datetime import datetime

from src.recorder import Recorder
from src.asr import WhisperCloud, Asr, Vosk, WhisperLocal
from src.gpt import Gpt
from src.tts import Tts
from src.audio_player import AudioPlayer
from utils import clear_line

from src.weather import get_weather


recorder = Recorder()
asr: Asr = WhisperLocal()
gpt = Gpt()
tts = Tts()
player = AudioPlayer()

def run_recorder():
    while True:
        byte = recorder.iter()
        if (byte):
            player.load_and_play_once("./assets/received.wav")
            input = asr(byte)
            print(clear_line + "You said: " + input)
            output = gpt(input)
            if output == "ring" or output == "beep":
                player.load_and_play_in_loop("./assets/ring.wav")
            elif output == "stop_ring":
                player.stop()
            elif output == "weather":
                weather = get_weather()
                output = gpt("weather\n" + weather)
                print(clear_line + "Assistant said: " + output)
                tts(output)
            elif output == "time":
                time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                output = gpt("time\n" + time)
                print(clear_line + "Assistant said: " + output)
                tts(output)
            else:
                print(clear_line + "Assistant said: " + output)
                tts(output)


def main():

    recorder.init()
    try:
        run_recorder()
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        recorder.terminate()


if __name__ == '__main__':
    main()
