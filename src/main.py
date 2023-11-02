from src.recorder import Recorder
from src.wav_file_writer import WavFileWriter
from src.asr import WhisperCloud, Asr
from src.gpt import Gpt
from src.tts import Tts
from src.audio_player import AudioPlayer
from utils import clear_line

wav_file_writer = WavFileWriter()
recorder = Recorder()
asr: Asr = WhisperCloud()
gpt = Gpt()
tts = Tts()
player = AudioPlayer()

def run_recorder():
    while True:
        byte = recorder.iter()
        if (byte):
            wav_file_writer(byte)
            input = asr("output.wav")
            print(clear_line + "You said: " + input)
            output = gpt(input)
            if output == "ring":
                player.load_and_play("./assets/ring.wav")
            elif output == "stop_ring":
                player.stop()
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
