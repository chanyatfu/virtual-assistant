import pyaudio
import numpy as np
import torch
from enum import Enum
from src.silero_vad import SileroVad
from src.vocal_activity import VocalActivity
from src.utils import clear_line
from src.wav_file_writer import WavFileWriter


class Recorder:
    
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK_DURATION_MS = 150
        self.PADDING_DURATION_MS = 1500
        self.CHUNK_SIZE = int(self.RATE * self.CHUNK_DURATION_MS / 1000)
        self.PADDING_CHUNKS = int(self.PADDING_DURATION_MS / self.CHUNK_DURATION_MS)

        self.remaining_padding = self.PADDING_CHUNKS
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.FORMAT,
                                      channels=self.CHANNELS,
                                      rate=self.RATE,
                                      input=True,
                                      start=False,
                                      frames_per_buffer=self.CHUNK_SIZE)
        self.active = False
        self.vad = SileroVad()
        self.buffer = []
        self.wav_file_writer = WavFileWriter()
        
    def reset_padding_chunks(self):
        self.remaining_padding = self.PADDING_CHUNKS
        
    def decrement_padding_chunks(self):
        self.remaining_padding -= 1
        
    def chunk_to_float_tensor(self, chunk):
        audio_int16 = np.frombuffer(chunk, np.int16)
        audio_float32 = self.int2float(audio_int16)
        return torch.from_numpy(audio_float32)
    
    def int2float(self, sound):
        abs_max = np.abs(sound).max()
        sound = sound.astype('float32')
        if abs_max > 0:
            sound *= 1/32768
        sound = sound.squeeze()
        return sound
    
    def read_stream(self):
        return self.stream.read(self.CHUNK_SIZE, exception_on_overflow=False)
    
    def stream_to_float_tensor(self, stream):
        return self.chunk_to_float_tensor(stream)
    
    def update_padding_chunks(self, vocal_activity):
        if vocal_activity == VocalActivity.UNVOICED:
            self.decrement_padding_chunks()
        else:
            self.reset_padding_chunks()
            
    def set_idle(self):
        self.active = False
        self.reset_padding_chunks()
        self.buffer.clear()
        
    def is_finished(self):
        return self.active and self.remaining_padding == 0
    
    def print_current_state_and_confidence(self, confidence):
        if self.active:
            print(f'{clear_line}Recording: {confidence}\r', end='')
        else:
            print(f'{clear_line}Idling : {confidence}\r', end='')
            
    def append_buffer(self, chunk):
        self.buffer.append(chunk)
        
    def get_buffer(self):
        return b''.join(self.buffer)
    
    def run(self):
        self.stream.start_stream()
        print('Listening (ctrl-C to exit)...')
        while True:
            chunk = self.read_stream()
            chunk_tensor = self.stream_to_float_tensor(chunk)
            confidence = self.vad(chunk_tensor, 16000).item()
            vocal_activity = VocalActivity.get_vocal_activity(confidence)
            
            if self.is_finished():
                self.wav_file_writer(self.get_buffer())
                self.set_idle()
            elif self.active:
                self.update_padding_chunks(vocal_activity)
                self.append_buffer(chunk)
            elif vocal_activity == VocalActivity.VOICED:
                self.active = True
                self.append_buffer(chunk)
            
            self.print_current_state_and_confidence(confidence)
    
    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
