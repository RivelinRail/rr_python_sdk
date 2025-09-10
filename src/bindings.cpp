#include <pybind11/pybind11.h>
#include "../extern/device-protocol/include/protocol/protocol.hpp"

namespace py = pybind11;
using namespace mh_protocol;

std::size_t payload_length_to_device(MsgType_ToDevice msg);
std::size_t payload_length_to_host(MsgType_ToHost msg);

//#include "generated_payload_switch.cpp"// switch functions

PYBIND11_MODULE(mh_protocol_py, m) {
    m.doc() = "Python bindings for mh_protocol";

    m.attr("MAX_MESSAGE_LENGTH") = MAX_MESSAGE_LENGTH;
    m.attr("N_FRAMING_START_BYTES") = N_FRAMING_START_BYTES;
    m.attr("SYNC_BYTE") = SYNC_BYTE;
    m.attr("N_CHECKSUM_BYTES") = N_CHECKSUM_BYTES;
    m.attr("MIN_MESSAGE_LENGTH") = MIN_MESSAGE_LENGTH;
    
    //m.attr("protocol_version_minor") = version.minor;
    //m.attr("protocol_version_patch") = version.patch;

    m.def("crc16_ccitt", [](py::bytes b) -> uint16_t {
        std::string s = b; // py::bytes converts to std::string
        const uint8_t* data = reinterpret_cast<const uint8_t*>(s.data());
        size_t len = s.size();
        return crc16_ccitt(data, len);
    }, py::arg("data"), "Compute CRC16/CCITT-FALSE over bytes");

    #include "generated_bindings.cpp"      // enums + structs

    m.attr("protocol_version") = version;
}
