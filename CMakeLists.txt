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

# --- Copy the compiled module into the Python package folder ---
# Adjust this path to wherever your Python package lives
set(PY_PACKAGE_DIR ${CMAKE_SOURCE_DIR}/rr_python_sdk)

add_custom_command(TARGET mh_protocol_py POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory ${PY_PACKAGE_DIR}
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:mh_protocol_py> ${PY_PACKAGE_DIR}/$<TARGET_FILE_NAME:mh_protocol_py>
    COMMENT "Copying mh_protocol_py module into Python package folder..."
)