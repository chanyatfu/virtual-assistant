import pygame
import threading

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()

    def load_and_play(self, filename):
        pygame.mixer.music.load(filename)
        threading.Thread(target=self._play).start()
    
    def _play(self):
        pygame.mixer.music.play(-1)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()
