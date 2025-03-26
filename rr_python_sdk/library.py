import serial
import struct
import time
from collections import namedtuple

__all__ = ["ForceDataPoint", "ConfigData", "MeasurmentHead"]

ForceDataPoint = namedtuple("ForceDataPoint", ["device_status", "ms_since_start", "f_n_mn", "f_t_mn", ])
OrientationData = namedtuple("OrientationData", ["incline", "roll", "creep_angle"])
LongStatus = namedtuple("LongStatus", ["device_status", "f_n", "f_t", "millis_since_start"])

CONFIG_FORMAT = "<I f f f f f f f f f f f I I f f f f f f"

class ConfigData:
    """Class to represent and update the sensor configuration."""
    def __init__(self, *args):
        fields = [
            "microsteps_per_step", "PID_P", "PID_I", "PID_D", "normal_max_load", "tangential_max_load", 
            "belt_ratio", "thread_pitch", "approach_speed", "home_speed", "normal_travel", "unload_travel", 
            "homing_timeout", "touch_force_mn", "max_deriv_control", "max_integral_error", 
            "max_acceleration", "max_speed", "n_force_scale", "t_force_scale"
        ]
        for field, value in zip(fields, args):
            setattr(self, field, value)
    
    def pack(self):
        """Pack the configuration data into a binary format for transmission."""
        return struct.pack(CONFIG_FORMAT, *self.__dict__.values())
    
    @classmethod
    def unpack(cls, data):
        """Unpack binary data into a ConfigData object."""
        values = struct.unpack(CONFIG_FORMAT, data)
        return cls(*values)


class MeasurmentHead:
    # Define the struct format (matching the C struct layout)
    # < - little-endian
    # B - uint8_t (1 byte)
    # H - uint16_t (2 bytes each, total 6 bytes)
    STRUCT_FORMATS = {
        b"<<P": "<HHii",
        b"<<C": CONFIG_FORMAT,
        b"<<E": "<I",
        b"<<O": "<ffB"
    }
    ACK = b"\6"
    NAK = b"\21"

    def __init__(self, port='/dev/ttyUSB0', baudrate=1000000, timeout=0.3):
        self.ser = serial.Serial(port, baudrate, timeout=timeout, parity=serial.PARITY_ODD)

    def read_all_input(self) -> bytes:
        return self.ser.readall()

    def wait_for_ack(self) -> bool:
        data = self.ser.read(1)
        if data==self.ACK:
            return True
        print(data)
        return False 

    def _read_struct(self, command:bytes, send_command:bool = True):
        """Generic function to request and read a structured response from the sensor."""
        if command not in self.STRUCT_FORMATS:
            raise ValueError("Unknown command.")
        if send_command:
            self.read_all_input()
            self.ser.write(command)

        format_str = self.STRUCT_FORMATS[command]
        size = struct.calcsize(format_str)
        data = self.ser.read(size + 2)
        
        if len(data) != size + 2:
            raise ValueError(f"Error: Incomplete data received for {command}\n"
                  f"Length expected {size + 2}, length recieved {len(data)}, data: {data.__repr__()}")
        
        if not data.startswith(b"<<"):
            raise ValueError(f"Recieved data dosn't start with correct sequence: {data.__repr__()}")
        data = data[2:]
        
        return struct.unpack(format_str, data)

    def n_calib_read(self):
        #TODO
        pass

    def n_calib_write(self):
        #TODO
        pass

    def t_calib_read(self):
        #TODO
        pass

    def T_calib_write(self):
        #TODO
        pass

    def o_calib_read(self):
        #TODO
        pass

    def o_calib_write(self):
        #TODO
        pass

    def set_angle(self, angle_mrad: float):
        char = int(angle_mrad)
        if char>255 or char<0:
            raise ValueError("Angle can only be set between 0 and 255 mrad")
        self.ser.write(b"<<A" + bytes([char]))
        self.wait_for_ack()

    def echo(self, message: bytes) -> bytes:
        self.ser.write(b"<<B" + message)
        time.sleep(0.1)
        rec = self.ser.read_all()
        return rec

    def read_config_data(self) -> ConfigData:
        data = self._read_struct(b"<<C")
        return ConfigData(*data)
    
    def update_config_data(self, config: ConfigData) -> bool:
        """Send an updated configuration to the device."""
        self.ser.write(b"<<c" + config.pack())
        return self.wait_for_ack()
    
    def start_streaming_force_data(self, data_rate: int):
        """Send command to start streaming data with a specified data rate (1-255 samples per second)."""
        if not (1 <= data_rate <= 255):
            raise ValueError("Data rate must be between 1 and 255.")
        self.ser.write(b"<<D" + bytes([data_rate]))

    def stop_streaming_force_data(self):
        self.ser.write(b"<<d")

    def read_force_data_point_from_stream(self) -> ForceDataPoint:
        return ForceDataPoint(*self._read_struct(b"<<P", False))

    def read_error_status(self):
        """read the error status of the device, can be shown with f"{head.read_error_status():016b}" """
        data = self._read_struct(b"<<E")
        return data[0]
        
    def clear_error_status(self) -> bool:
        """Reset the sensor's error status."""
        self.ser.write(b"<<e")
        return self.wait_for_ack()
    
    def set_target_force(self, force_mn: float) -> bool:
        """Send a target force command to the device."""
        force_bytes = struct.pack("<I", abs(int(force_mn)))
        self.ser.write(b"<<F" + force_bytes)
        return self.wait_for_ack()

    def read_long_status(self) -> LongStatus:
        raise NotImplementedError("Not implemented yet")
    
    def clear_long_status(self):
        raise NotImplementedError("Not implemented yet")
    
    def home(self) -> bool:
        self.read_all_input()
        self.ser.write(b"<<H")
        return self.wait_for_ack()
    
    def jog(self, steps:int) -> bool:
        steps_bytes = struct.pack("<i", steps)
        self.ser.write(b"<<J" + steps_bytes)
        return self.wait_for_ack()
    
    def toggle_led(self, led: bool) -> bool:
        self.ser.write(b"<<L" + (b"\1" if led else b"\0"))
        return self.wait_for_ack()
    
    def stop_all(self) -> bool:
        self.ser.write(b"<<N")
        return self.wait_for_ack()
    
    def read_orientation_data(self):
        return OrientationData(*self._read_struct(b"<<O"))
    
    def read_single_force_data_point(self) -> ForceDataPoint:
        """Only to be used when device isn't streaming"""
        return ForceDataPoint(*self._read_struct(b"<<P"))
    
    def restart(self)-> bool:
        self.ser.write(b"<<R")
        return self.wait_for_ack()

    def maintain_force(self, force_mn:float):
        self.set_target_force(force_mn)
        self.ser.write(b"<<S")
        return self.wait_for_ack()
    
    def zero_forces(self) -> bool:
        self.read_all_input()
        self.ser.write(b"<<Z")
        return self.wait_for_ack()

    def close(self):
        self.ser.close()