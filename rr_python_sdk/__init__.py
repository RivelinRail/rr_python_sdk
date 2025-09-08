# measurement_head/__init__.py

from .wrapper import MeasurementHead, cpp
from pathlib import Path
import re

# --- Helpers from wrapper.py ---
def cpp_to_python_name(name: str) -> str:
    if name.endswith("_t"):
        name = name[:-2]
    parts = name.split('_')
    return ''.join(p.capitalize() for p in parts)

def camel_to_snake_case(s1):
    if s1 == "ACK":
        return "ack"
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
        msg_map[enum_name] = (py_name, payload_name)
    return msg_map

# --- Attach SendX methods at import ---
header_path = Path(__file__).resolve().parents[1] / "extern/device-protocol/include/protocol/msg_info_to_device.hpp"
msg_map = parse_msg_info(header_path)

def attach_send_methods(cls, msg_map):
    from types import MethodType
    for enum_name, (py_struct_name, payload_name) in msg_map.items():
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

attach_send_methods(MeasurementHead, msg_map)

# --- Expose MeasurementHead at package level ---
__all__ = ["MeasurementHead", "cpp"]
