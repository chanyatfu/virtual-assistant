import unittest
from src.core.gpt import Gpt

class TestGpt(unittest.TestCase):
    def test_weather(self):
        gpt = Gpt()
        self.assertEqual(gpt("How is the weather today."), "weather")

    def test_time(self):
        gpt = Gpt()
        self.assertEqual(gpt("What time is it."), "time")

    def test_ring(self):
        gpt = Gpt()
        self.assertEqual(gpt("Where are you?"), second="ring")

    def test_stop_ring(self):
        gpt = Gpt()
        self.assertEqual(gpt("Stop ringing"), second="stop_ring")

