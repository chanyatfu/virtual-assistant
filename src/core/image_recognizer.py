from typing import Any
import threading
from src.helpers.concurrent_decor import concurrent

class ImageRecognizer:
    def __init__(self, rate=16000):
        self.rate = rate
        self.buffer: list[dict] = []

    @concurrent
    def run(self) -> None:
        while True:
            self._recognize()

    def fetch(self) -> list[dict]:
        # return the content of the output buffer
        return self.buffer

    def _recognize(self) -> None:
        # recognize the image and update the buffer
        pass
