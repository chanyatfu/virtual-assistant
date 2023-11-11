from pyannote.audio import Pipeline
from typing import Any
from dotenv import load_dotenv
import os
import torch

load_dotenv(".env.local")

class PyannoteVad:
    def __init__(self) -> None:
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/voice-activity-detection",
            use_auth_token=os.getenv("HUGGING_FACE_USE_AUTH_TOKEN"))

    def __call__(self, chunk_tensor: torch.Tensor, sample_rate=16000) -> Any:
        ret = self.pipeline({
            "waveform": chunk_tensor.unsqueeze(0),
            "sample_rate": sample_rate,
        })
        for speech in ret.get_timeline().support():
            print(speech)
        # print(ret)
        return ret
