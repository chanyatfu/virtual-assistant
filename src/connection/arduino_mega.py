import serial

class ArduinoMegaUart:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS0', 9600)

    def __call__(self, data_to_send: str):
        self.ser.write(data_to_send.encode())

    def close(self):
        self.ser.close()
