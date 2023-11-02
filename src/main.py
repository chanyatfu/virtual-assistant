from src.recorder import Recorder
from src.wav_file_writer import WavFileWriter
from src.transcripter import WhisperCloud
from src.gpt import Gpt
from src.tts import Tts
from utils import clear_line

def run_recorder(recorder: Recorder, wav_file_writer: WavFileWriter, transcripter: WhisperCloud, gpt: Gpt, tts: Tts):
    while True:
        byte = recorder.iter()
        if (byte):
            wav_file_writer(byte)
            input = transcripter("output.wav")
            print(clear_line + "You said: " + input)
            output = gpt(input)
            print(clear_line + "Assistant said: " + output)
            tts(output)


def main():
    wav_file_writer = WavFileWriter()
    recorder = Recorder()
    transcripter = WhisperCloud()
    gpt = Gpt()
    tts = Tts()
    recorder.init()
    
    try:
        run_recorder(recorder, wav_file_writer, transcripter, gpt, tts)
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        recorder.terminate()


if __name__ == '__main__':
    main()
