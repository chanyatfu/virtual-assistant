import pygame
import threading

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()

    def load_and_play_once(self, filename):
        pygame.mixer.music.load(filename)
        threading.Thread(target=self._play_once).start()

    def _play_once(self):
        pygame.mixer.music.play(0)

    def load_and_play_in_loop(self, filename):
        pygame.mixer.music.load(filename)
        threading.Thread(target=self._play_in_loop).start()

    def _play_in_loop(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()
