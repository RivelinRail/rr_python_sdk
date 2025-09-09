# measurement_head/__init__.py

from .wrapper import MeasurementHead, cpp
from pathlib import Path
import re
from types import MethodType

# --- Helpers from wrapper.py ---
def cpp_to_python_name(name: str) -> str:
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

def parse_msg_info(header_path: Path):
    text = header_path.read_text()
    msg_map = {}
    for enum_name, payload_name in MSG_INFO_RE.findall(text):
        py_name = cpp_to_python_name(payload_name.split("::")[-1])
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
            def send_method(self):
                msg_enum = getattr(cpp, enum_name)
                frame = bytes([msg_enum])
                self.ser.write(frame)
        else:
            def send_method(self, payload):
                if not isinstance(payload, getattr(cpp, py_struct_name)):
                    raise ValueError(f"{method_name} can only be called with an argument of type {py_struct_name}")
                msg_enum = getattr(cpp, enum_name)
                frame = bytes([msg_enum]) + payload.serialize()
                self.ser.write(frame)

        setattr(cls, method_name, MethodType(send_method, cls))

attach_send_methods(MeasurementHead, msg_map_to_device)

# --- Attach receive methods ---
header_host = Path(__file__).resolve().parents[1] / "extern/device-protocol/include/protocol/msg_info_to_host.hpp"
msg_map_to_host = parse_msg_info(header_host)

def read(self):
    """Read one message and return parsed struct or None."""
    tag_bytes = self.ser.read(1)
    if not tag_bytes:
        return None  # no data
    tag = tag_bytes[0]

    if tag not in msg_map_to_host:
        return None  # unknown type, skip

    struct_cls = getattr(cpp, msg_map_to_host[tag])
    length = struct_cls.sizeof()  # pybind-bound method
    payload = self.ser.read(length)
    if len(payload) < length:
        return None  # incomplete

    return struct_cls.deserialize(payload)

def read_all(self):
    """Read everything in buffer, return list of parsed structs."""
    messages = []
    while True:
        msg = self.read()
        if msg is None:
            break
        messages.append(msg)
    return messages

setattr(MeasurementHead, "read", MethodType(read, MeasurementHead))
setattr(MeasurementHead, "read_all", MethodType(read_all, MeasurementHead))

# --- Expose MeasurementHead at package level ---
__all__ = ["MeasurementHead", "cpp"]
