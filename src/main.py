from src.recorder import Recorder

def main():
    recorder = Recorder()
    try:
        recorder.run()
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        recorder.terminate()


if __name__ == '__main__':
    main()
