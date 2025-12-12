from . import mh_protocol_py as cpp
import serial
import serial.tools.list_ports
import datetime
import warnings
from typing import Optional

# --- MeasurementHead class ---
class MeasurementHead:
    handshake_response = None

    def __init__(self, port: Optional[str] = None, baudrate: int = 1_000_000):
        if port is None:
            port = self._get_serial_port()
        if port is None:
            raise ValueError("Could not detect device")
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=1, write_timeout=1)
        if not self.shakehands():
            warnings.warn("Handshake not acknowledged, device not ready")

    def _get_serial_port(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            print(p.description, p.vid)
            if "USB Serial Port" in p.description and p.vid == 1027:
                print(f"Auto detected: {p.description}")
                return p.device
        return None

    def shakehands(self):
        self.ser.read_all()

        now = datetime.datetime.now()

        payload = cpp.HandshakeToDevicePayload()
        payload.protocol_version = cpp.protocol_version
        #payload.protocol_version.minor = cpp.protocol_version_minor
        #payload.protocol_version.patch = cpp.protocol_version_patch
        payload.date.day_y = now.timetuple().tm_yday
        payload.date.year = now.year
        payload.hour = now.hour
        payload.minute = now.minute
        payload.second = now.second

        # --- Send handshake ---
        self.handshake(payload)

        ack = False
        resps = self.read_all(cpp.MsgType_ToHost.Handshake, 3)
        for resp in resps:
            if resp.type == cpp.MsgType_ToHost.Handshake:
                print("Handshake acknowledged:", resp.data)
                ack = True
                self.handshake_response = resp.data
            elif resp.type == cpp.MsgType_ToHost.ERR:
                print("Error response received:", resp.type, resp.data.reason)
            elif resp.type == cpp.MsgType_ToHost.FaultData:
                print("Device fault", resp.data.fault_status)
            else:
                print("Unknown response received:", resp.type, resp.data)
        return ack


    def close(self):
        self.ser.close()
