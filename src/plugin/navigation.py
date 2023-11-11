from uuid import UUID
from src.core.image_recognizer import ImageRecognizer

class Navigator:
    def __init__(self):
        self.image_recongnizer = ImageRecognizer()
        self.destination = None
        self.arrived = False

    def set_destination(self, destination: UUID):
        self.destination = destination

    def navigate(self):
        while not self.arrived:
            pass

    

    def _update_position(self):
        pass

