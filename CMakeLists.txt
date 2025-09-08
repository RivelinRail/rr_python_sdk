cmake_minimum_required(VERSION 3.15)
project(mh_protocol_py LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# pybind11
add_subdirectory(extern/pybind11)
#find_package(pybind11 CONFIG REQUIRED)

# Add submodule include
add_subdirectory(extern/device-protocol)

# Build Python extension
pybind11_add_module(mh_protocol_py src/bindings.cpp)

# Make sure compiler can see device-protocol headers
target_include_directories(mh_protocol_py PRIVATE extern/device-protocol)
target_link_libraries(mh_protocol_py PRIVATE device-protocol)  # if submodule builds a lib
