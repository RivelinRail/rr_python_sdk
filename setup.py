import os
import sys
import subprocess
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeBuild(build_ext):
    def run(self):
        # 1. Run the generator
        subprocess.check_call([sys.executable, os.path.join("tools", "gen_pybind_glue.py")])

        # 2. Configure and build CMake
        build_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "build")
        os.makedirs(build_dir, exist_ok=True)
        subprocess.check_call(["cmake", "../", "-B", build_dir])
        subprocess.check_call(["cmake", "--build", build_dir, "--config", "Release"])

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setup(
    name="rr_python_sdk",
    version="0.1.0",
    author="Mike Watson",
    author_email="m.watson@rivelinrail.com",
    description="Python functions for interfacing with the measurement head",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mikeWShef/RR_measurment_head_python",
    project_urls={
        "Bug Tracker": "https://github.com/mikeWShef/RR_measurment_head_python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyserial"],
    packages=["rr_python_sdk"],
    cmdclass={"build_ext": CMakeBuild},
    python_requires=">=3.6",
)