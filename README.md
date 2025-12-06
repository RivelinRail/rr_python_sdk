# RR Measurement Head Python SDK

Python package for interfacing with the Rivelin Rail measurement head device.
Provides both high-level Python APIs for sending/receiving messages and access to the underlying C++ protocol via pybind11.

---

## Features

- Send commands to the device using structured payloads.
- Read structured messages from the device.
- Automatic CRC-16 checking and framing.
- Pythonic wrapper around the C++ protocol.
- Dynamically generated methods for all supported send and receive messages.

---

## Requirements

### Build Requirements

- Python 3.8+
- A C++17 compatible compiler toolchain
- `pip`, `setuptools`, `wheel`, and `pybind11` (automatically pulled in as build dependencies)

### Python Package Requirements

- `pyserial` for serial communication

---

## Installation

The release versions are available as Release artifacts from the [Github Releases](https://github.com/RivelinRail/rr_python_sdk/releases).
Choose the appropriate zip file for your Operating System and architecture.

After downloading the zip, unzip it and use the wheel matching your python version in the next step.

### Install the published wheel

```bash
python -m pip install ./<wheel name>.whl
```

The published wheels already contain the compiled `mh_protocol_py` extension for common platforms.

### Build from source

```bash
git clone --recurse-submodules https://github.com/RivelinRail/rr_python_sdk.git
cd rr_python_sdk

# Option A: editable install for development
python -m pip install --upgrade pip
python -m pip install -e .

# Option B: build distributable artifacts
python -m pip install build
python -m build
```

During the build step, the `tools/gen_pybind_glue.py` script runs automatically to regenerate `src/generated_bindings.cpp`, and setuptools uses pybind11's include paths provided by the dependency.

## Usage

```python

from rr_python_sdk import cpp, MeasurementHead

# --- Initialize serial connection and handshake with the device ---
head = MeasurementHead("COM3")  # Replace with your serial port

# --- Send a message with no data ---
head.home()

# --- Read a message ---
message = head.read()

# --- Send a message with data ---
payload = cpp.JogPayload()
payload.distance_mm = 1.0
head.jog_motor(payload)

# --- Close connection ---
head.close()

```

## Structure

* `rr_python_sdk/` - Python package

  * `wrapper.py` – high-level class for serial communication
  * `mh_protocol_py.*` – compiled C++ extension via pybind11
* `tools/gen_pybind_glue.py` – generates pybind11 bindings for structs and enums
* `extern/device-protocol/` – C++ device protocol submodule
* `src/` – generated C++ glue code

---

## Notes

* The C++ extension exposes all protocol enums and payload structs.
* Messages are automatically framed with sync bytes (`0xAA 0xAA`) and CRC-16 checksums.
* Python methods are dynamically generated for all sendable messages based on the C++ protocol definitions.

---

## License

MIT License

---
