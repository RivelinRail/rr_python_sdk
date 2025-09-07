#!/usr/bin/env python3
import re
from pathlib import Path

# crude regexes; good enough for enum/struct prototypes without macros
ENUM_RE = re.compile(r'enum\s+class\s+(\w+)\s*:\s*\w+\s*\{([^}]*)\}', re.DOTALL)
STRUCT_RE = re.compile(r'struct\s+(\w+)\s*\{([^}]*)\}', re.DOTALL)
FIELD_RE = re.compile(r'([A-Za-z_]\w*)\s+([A-Za-z_]\w*)\s*;')

def parse_enums(text):
    enums = {}
    for name, body in ENUM_RE.findall(text):
        entries = []
        for line in body.split(','):
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            if '=' in line:
                ident, val = line.split('=', 1)
                entries.append(ident.strip())
            else:
                entries.append(line.strip())
        enums[name] = entries
    return enums

def parse_structs(text):
    structs = {}
    for name, body in STRUCT_RE.findall(text):
        fields = []
        for type_, ident in FIELD_RE.findall(body):
            fields.append((type_, ident))
        structs[name] = fields
    return structs

def main():
    root = Path(__file__).resolve().parents[1]
    # adjust to your header locations
    text = (root / "extern" / "device-protocol" / "include" / "protocol" / "message_types.hpp").read_text()
    text += (root / "extern" /"device-protocol" / "include" / "protocol" / "measurement_head_types.hpp").read_text()

    enums = parse_enums(text)
    structs = parse_structs(text)

    out_lines = []
    # generate enums
    for enum_name, entries in enums.items():
        out_lines.append(f'py::enum_<{enum_name}>(m, "{enum_name}")')
        for e in entries:
            out_lines.append(f'    .value("{e}", {enum_name}::{e})')
        out_lines.append('    ;\n')

    # generate structs
    for struct_name, fields in structs.items():
        out_lines.append(f'py::class_<{struct_name}>(m, "{struct_name}")')
        out_lines.append('    .def(py::init<>())')
        for type_, ident in fields:
            out_lines.append(f'    .def_readwrite("{ident}", &{struct_name}::{ident})')
        out_lines.append('    ;\n')

    Path("src/generated_bindings.cpp").write_text("\n".join(out_lines))
    print("Wrote src/generated_bindings.cpp")

if __name__ == "__main__":
    main()
