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

- Python 3.6+
- CMake >= 3.15
- A C++17 compatible compiler
- `pybind11` (handled via build dependencies)
- `setuptools` and `wheel`

### Python Package Requirements

- `pyserial` for serial communication

---

## Installation

Clone the repository:

```bash
git clone --recurse-submodules https://github.com/RivelinRail/rr_python_sdk.git
cd RR_measurment_head_python
```

Install the package:

```bash
pip install .
```

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
payload = cpp.JogPayload
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