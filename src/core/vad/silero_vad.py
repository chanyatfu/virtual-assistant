import torch
from typing import Any

class SileroVad:
    def __init__(self):
        self.model, self.utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=True)
        (self.get_speech_timestamps,
        self.save_audio,
        self.read_audio,
        self.VADIterator,
        self.collect_chunks) = self.utils

    def __call__(self, chunk_tensor, sample_rate=16000) -> Any:
        return self.model(chunk_tensor, sample_rate).item()
