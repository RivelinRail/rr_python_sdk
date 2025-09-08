#include <pybind11/pybind11.h>
#include "../extern/device-protocol/include/protocol/protocol.hpp"

namespace py = pybind11;
using namespace mh_protocol;

std::size_t payload_length_to_device(MsgType_ToDevice msg);
std::size_t payload_length_to_host(MsgType_ToHost msg);

#include "generated_payload_switch.cpp"// switch functions

PYBIND11_MODULE(mh_protocol_py, m) {
    m.doc() = "Python bindings for mh_protocol";

    #include "generated_bindings.cpp"      // enums + structs

    // expose as Python functions
    m.def("payload_length_to_device", &payload_length_to_device);
    m.def("payload_length_to_host", &payload_length_to_host);
}
