from enum import Enum

class VocalActivity(Enum):
    UNVOICED = 1
    MIXED = 2
    VOICED = 3
    
    @staticmethod
    def get_vocal_activity(confidence: float):
        if confidence > 0.7:
            return VocalActivity.VOICED
        elif confidence < 0.2:
            return VocalActivity.UNVOICED
        else:
            return VocalActivity.MIXED
