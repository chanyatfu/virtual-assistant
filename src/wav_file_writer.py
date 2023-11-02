import wave
import pyaudio

class WavFileWriter:
    def __init__(self, channels=1, rate=16000, sample_width=2, format=pyaudio.paInt16):
        self.channels = channels
        self.rate = rate
        self.format = format
        self.sample_width = sample_width
        
    def __call__(self, frames, filename="output.wav",):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(frames)
        wf.close()

    