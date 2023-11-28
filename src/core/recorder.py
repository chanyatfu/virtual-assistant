import pyaudio
import numpy as np
import torch
from typing import Optional, List
from src.core.vad import SileroVad, PyannoteVad
from src.core.vocal_activity import VocalActivity
from src.helpers.clear_line import clear_line

class Recorder:

    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK_DURATION_MS = 150
        self.PADDING_DURATION_MS = 300
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
        self.buffer: List[bytes] = []
        self.finished = False

    def init(self) -> None:
        self.stream.start_stream()
        print('Listening (ctrl-C to exit)...')

    def iter(self) -> Optional[bytes]:
        if (not self.active):
            self.finished = False
            self.buffer.clear()
        chunk = self._read_stream()
        chunk_tensor = self._stream_to_float_tensor(chunk)
        confidence = self.vad(chunk_tensor)
        vocal_activity = VocalActivity.get_vocal_activity(confidence)
        self._append_buffer(chunk)

        if self._is_finished():
            self.finished = True
            self._set_idle()
        elif self.active:
            self._update_padding_chunks(vocal_activity)
        elif (not self.active) and (vocal_activity == VocalActivity.VOICED):
            self.active = True
        else:
            self._print_current_state_and_confidence(confidence)
            return None

        self._print_current_state_and_confidence(confidence)
        return chunk

    def terminate(self) -> None:
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def _reset_padding_chunks(self) -> None:
        self.remaining_padding = self.PADDING_CHUNKS

    def _decrement_padding_chunks(self) -> None:
        self.remaining_padding -= 1

    def _chunk_to_float_tensor(self, chunk: bytes) -> torch.Tensor:
        audio_int16 = np.frombuffer(chunk, np.int16)
        audio_float32 = self._int2float(audio_int16)
        return torch.from_numpy(audio_float32)

    def _int2float(self, sound: np.ndarray) -> np.ndarray:
        abs_max = np.abs(sound).max()
        sound = sound.astype('float32')
        if abs_max > 0:
            sound *= 1/32768
        sound = sound.squeeze()
        return sound

    def _read_stream(self) -> bytes:
        return self.stream.read(self.CHUNK_SIZE, exception_on_overflow=False)

    def _stream_to_float_tensor(self, stream: bytes) -> torch.Tensor:
        return self._chunk_to_float_tensor(stream)

    def _update_padding_chunks(self, vocal_activity: VocalActivity) -> None:
        if vocal_activity == VocalActivity.UNVOICED:
            self._decrement_padding_chunks()
        else:
            self._reset_padding_chunks()

    def _set_idle(self) -> None:
        self.active = False
        self._reset_padding_chunks()
        # self.buffer.clear()

    def _is_finished(self) -> bool:
        return self.active and self.remaining_padding == 0

    def _print_current_state_and_confidence(self, confidence: float) -> None:
        if self.active:
            print(f'{clear_line}Recording: {confidence}', end='\r', flush=True)
        else:
            print(f'{clear_line}Idling : {confidence}', end='\r', flush=True)

    def _append_buffer(self, chunk: bytes) -> None:
        self.buffer.append(chunk)

    def _get_buffer(self) -> bytes:
        return b''.join(self.buffer)

    def _get_buffer_and_cleanup(self) -> bytes:
        buffer = self._get_buffer()
        self._set_idle()
        return buffer
