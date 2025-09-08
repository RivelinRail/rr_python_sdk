from . import mh_protocol_py as cpp
import re
import serial
from pathlib import Path
from types import MethodType

# --- MeasurementHead class ---
class MeasurementHead:
    def __init__(self, port: str, baudrate: int = 1_000_000):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=1)
        

    def close(self):
        self.ser.close()
