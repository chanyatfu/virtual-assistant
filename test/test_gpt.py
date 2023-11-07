import unittest
from src.core.gpt import Gpt
import time

class TestGpt(unittest.TestCase):
    def setUp(self):
        self.gpt = Gpt()
        self._start_time = time.time()

    def tearDown(self) -> None:
        t = time.time() - self._start_time
        print(f"{self.id()}: {t:.3f}s")

class TestGptWeather(TestGpt):
    def test_weather(self):
        gpt = Gpt()
        self.assertEqual(gpt("How is the weather today."), "weather")


class TestGptTime(TestGpt):
    def test_time(self):
        gpt = Gpt()
        self.assertEqual(gpt("What time is it."), "time")

class TestGptRing(TestGpt):
    def test_ring1(self):
        gpt = Gpt()
        self.assertEqual(gpt("Where are you?"), second="ring")

    def test_ring2(self):
        gpt = Gpt()
        self.assertEqual(gpt("Ring."), second="ring")

class TestGptStopRing(TestGpt):
    def test_stop_ring1(self):
        gpt = Gpt()
        self.assertEqual(gpt("Stop ringing."), second="stop_ring")

    def test_stop_ring2(self):
        gpt = Gpt()
        self.assertEqual(gpt("Stop it."), second="stop_ring")
