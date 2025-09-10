from . import mh_protocol_py as cpp
import serial
import datetime

# --- MeasurementHead class ---
class MeasurementHead:
    def __init__(self, port: str, baudrate: int = 1_000_000):
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=1)
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

        # (Optional) wait for handshake response from device
        resp = self.read()
        if resp.type == cpp.MsgType_ToHost.Handshake:
            print("Handshake acknowledged:", resp.data)
        elif resp.type == cpp.MsgType_ToHost.ERR:
            print("Error response received:", resp.type, resp.data.reason)
        elif resp.type == cpp.MsgType_ToHost.FaultData:
            print("Device fault", resp.data.fault_status)
        else:
            print("Unknown response received:", resp.type, resp.data)

    def close(self):
        self.ser.close()
