from src.recorder import Recorder
from src.wav_file_writer import WavFileWriter

def run_recorder(recorder: Recorder, wav_file_writer: WavFileWriter):
    while True:
        byte = recorder.iter()
        if (byte):
            wav_file_writer(byte)

def main():
    wav_file_writer = WavFileWriter()
    recorder = Recorder()
    recorder.init()
    
    try:
        run_recorder(recorder, wav_file_writer)
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        recorder.terminate()


if __name__ == '__main__':
    main()
