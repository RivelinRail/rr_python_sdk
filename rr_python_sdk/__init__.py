# measurement_head/__init__.py

from .wrapper import MeasurementHead, cpp
from pathlib import Path
import re
from types import MethodType
from collections import namedtuple

# --- Helpers from wrapper.py ---
def snake_to_camel_case(name: str) -> str:
    if name.endswith("_t"):
        name = name[:-2]
    parts = name.split('_')
    return ''.join(p.capitalize() for p in parts)

def camel_to_snake_case(s1):
    if s1 == "ACK":
        return "ack"
    
    if s1 == "NAK":
        return "nak"
    
    if s1 == "ToggleLED":
        return "toggle_led"
    
    s2 = ''.join(['_' + char.lower() if char.isupper() else char for char in s1])

    if s2.startswith("_"):
        s2 = s2[1:]

    return s2


# --- Parse MSG_INFO_TO_DEVICE macros ---
MSG_INFO_RE = re.compile(r'MSG_INFO_TO_DEVICE\s*\(\s*([\w:]+)\s*,\s*([\w:]+)\s*\)')

def parse_msg_info(header_path: Path, byte_keys = False):
    text = header_path.read_text()
    msg_map = {}
    for enum_name, payload_name in MSG_INFO_RE.findall(text):
        py_name = snake_to_camel_case(payload_name.split("::")[-1])
        if (byte_keys):
            try:
                msg_map[int(getattr(cpp.MsgType_ToHost, enum_name))] = py_name
            except ValueError:
                pass
        else:
            msg_map[enum_name] = py_name
    return msg_map

# --- Attach send methods at import ---
header_device = Path(__file__).resolve().parents[1] / "extern/device-protocol/include/protocol/msg_info_to_device.hpp"
msg_map_to_device = parse_msg_info(header_device)

def attach_send_methods(cls, msg_map):
    for enum_name, py_struct_name in msg_map.items():
        enum_name = enum_name.split("::")[-1]

        if enum_name == "MSG_TYPE":
            continue

        method_name = camel_to_snake_case(enum_name)

        if (py_struct_name == "EmptyPayload"):
            def send_method(self, enum_name = enum_name):
                msg_enum = getattr(cpp.MsgType_ToDevice, enum_name)
                frame = bytes([cpp.SYNC_BYTE]*cpp.N_FRAMING_START_BYTES + [msg_enum])
                
                # Compute CRC16 over TYPE only
                crc = cpp.crc16_ccitt(frame[cpp.N_FRAMING_START_BYTES:])
                frame += bytes([ (crc >> 8) & 0xFF, crc & 0xFF ])

                self.ser.write(frame)
        else:
            def send_method(self, payload, enum_name = enum_name, py_struct_name = py_struct_name):
                if not isinstance(payload, getattr(cpp, py_struct_name)):
                    raise ValueError(f"{method_name} can only be called with an argument of type {py_struct_name}")
                
                msg_enum = getattr(cpp, enum_name)
                frame = bytes([cpp.SYNC_BYTE]*cpp.N_FRAMING_START_BYTES + [msg_enum]) + payload.serialize()

                crc = cpp.crc16_ccitt(frame[cpp.N_FRAMING_START_BYTES:])
                frame += bytes([ (crc >> 8) & 0xFF, crc & 0xFF ])

                self.ser.write(frame)

        setattr(cls, method_name, send_method)

attach_send_methods(MeasurementHead, msg_map_to_device)

# --- Attach receive methods ---
header_host = Path(__file__).resolve().parents[1] / "extern/device-protocol/include/protocol/msg_info_to_host.hpp"
msg_map_to_host = parse_msg_info(header_host, True)

Message = namedtuple("Message", ["type", "data"])

def read(self) -> Message:
    """Read one message and return parsed struct or None."""
    # --- Wait for sync bytes ---
    while True:
        sync = self.ser.read(1)
        if not sync:
            return Message(cpp.MsgType_ToHost.NoMessage, 0)
        if sync[0] == cpp.SYNC_BYTE:
            next_byte = self.ser.read(1)
            if not next_byte:
                return Message(cpp.MsgType_ToHost.NoMessage, 1)
            if next_byte[0] == cpp.SYNC_BYTE:
                break
            # otherwise continue scanning

    # --- Read type ---
    tag_bytes = self.ser.read(1)
    if not tag_bytes:
        return Message(cpp.MsgType_ToHost.NoMessage, 3)
    msg_type = tag_bytes[0]

    try:
        cpp_msg_type = cpp.MsgType_ToHost(msg_type)
    except ValueError:
        return Message(cpp.MsgType_ToHost.Unknown, None)

    if cpp_msg_type not in msg_map_to_host:
        return Message(cpp.MsgType_ToHost.Unknown, None)

    # --- Determine payload length ---
    struct_cls = getattr(cpp, msg_map_to_host[cpp_msg_type])
    length = struct_cls.sizeof()  # pybind-bound method

    # --- Read payload + CRC16 ---
    remaining_bytes = self.ser.read(length + cpp.N_CHECKSUM_BYTES)
    if len(remaining_bytes) < length + cpp.N_CHECKSUM_BYTES:
        return Message(cpp.MsgType_ToHost.FramingError, bytes([msg_type]) + remaining_bytes)

    payload_bytes = remaining_bytes[:length]

    # get recieved CRC
    rx_crc_bytes = remaining_bytes[length:length + 2]
    rx_crc = (rx_crc_bytes[0] << 8) | rx_crc_bytes[1]

    # --- Compute CRC16 over TYPE + PAYLOAD ---
    crc_input = bytes([msg_type]) + payload_bytes
    calc_crc = cpp.crc16_ccitt(crc_input)
    if rx_crc != calc_crc:
        return Message(cpp.MsgType_ToHost.CRCError, bytes([msg_type]) + remaining_bytes)

    # --- Deserialize payload ---
    if length == 0:
        return Message(cpp_msg_type, struct_cls())  # empty payload
    return Message(cpp_msg_type, struct_cls.deserialize(payload_bytes))

def read_all(self):
    """Read everything in buffer, return list of parsed structs."""
    messages = []
    while True:
        msg = self.read()
        if msg is None:
            break
        messages.append(msg)
    return messages

setattr(MeasurementHead, "read", read)
setattr(MeasurementHead, "read_all", read_all)

# --- Expose MeasurementHead at package level ---
__all__ = ["MeasurementHead", "cpp"]
