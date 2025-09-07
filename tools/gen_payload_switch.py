#!/usr/bin/env python3
import re
from pathlib import Path

ENUM_RE = re.compile(r'enum\s+class\s+(\w+)\s*:\s*\w+\s*\{([^}]*)\}', re.DOTALL)

def parse_enums(text):
    enums = {}
    for name, body in ENUM_RE.findall(text):
        entries = []
        for raw in body.split(','):
            raw = raw.strip()
            if not raw or raw.startswith('//'):
                continue
            # strip inline comments & assignment
            raw = raw.split('=')[0].strip()
            entries.append(raw)
        enums[name] = entries
    return enums

def main():
    root = Path(__file__).resolve().parents[1]
    header = (root / "extern" / "device-protocol" / "include" / "protocol" / "message_types.hpp").read_text()
    enums = parse_enums(header)

    out = []

    # --- MsgType_ToDevice ---
    if "MsgType_ToDevice" in enums:
        out.append("std::size_t payload_length_to_device(MsgType_ToDevice msg) {")
        out.append("    switch (msg) {")
        for e in enums["MsgType_ToDevice"]:
            out.append(f"        case MsgType_ToDevice::{e}: "
                       f"return MsgInfoToDevice<MsgType_ToDevice::{e}>::Length;")
        out.append("        default: return 0;")
        out.append("    }")
        out.append("}\n")

    # --- MsgType_ToHost ---
    if "MsgType_ToHost" in enums:
        out.append("std::size_t payload_length_to_host(MsgType_ToHost msg) {")
        out.append("    switch (msg) {")
        for e in enums["MsgType_ToHost"]:
            out.append(f"        case MsgType_ToHost::{e}: "
                       f"return MsgInfoToHost<MsgType_ToHost::{e}>::Length;")
        out.append("        default: return 0;")
        out.append("    }")
        out.append("}\n")

    Path("src/generated_payload_switch.cpp").write_text("\n".join(out))
    print("Wrote src/generated_payload_switch.cpp")

if __name__ == "__main__":
    main()
