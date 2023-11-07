import serial

class ArduinoMegaUart:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS0', 9600)

    def __call__(self, data_to_send: str):
        self.ser.write(data_to_send.encode())

    def close(self):
        self.ser.close()


class WheelController:
    bt_data = {
        "forward": "A",
        "forward-left": "H",
        "forward-right": "B",
        "left": "C",
        "right": "d",
        "backward": "E",
        "backward-left": "F",
        "backward-right": "D",
        "stop": "Z",
        "rotate-clockwise": "C",
        "rotate-anticlockwise": "D",
    }
    def __init__(self, uart: ArduinoMegaUart):
        self.uart = uart

    def __call__(self, command: str):
        if command in self.bt_data:
            self.uart(self.bt_data[command])
        else:
            raise ValueError(f"Invalid command: {command}")
