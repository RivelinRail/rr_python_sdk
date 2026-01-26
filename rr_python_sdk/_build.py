from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GLUE_SCRIPT = PROJECT_ROOT / "tools" / "gen_pybind_glue.py"


def _generate_bindings() -> None:
    subprocess.check_call([sys.executable, str(GLUE_SCRIPT)], cwd=PROJECT_ROOT)


def _copy_headers(build_root: Path) -> None:
    """Copy public C++ headers into the built wheel for downstream use."""

    src = PROJECT_ROOT / "extern" / "device-protocol" / "include"
    if not src.exists():  # pragma: no cover - defensive guard for CI
        raise FileNotFoundError(f"Missing header directory: {src}")

    dst_root = build_root / "rr_python_sdk" / "include"
    for header in src.rglob("*"):
        if not header.is_file():
            continue
        rel = header.relative_to(src)
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(header, dst)


class BuildExt(build_ext):
    """Run the code generator and ensure extensions compile with C++17."""

    _c_opts = {
        "msvc": ["/std:c++17"],
        "unix": ["-std=c++17"],
    }

    def run(self) -> None:
        _generate_bindings()
        super().run()

    def build_extensions(self) -> None:
        compiler_type = self.compiler.compiler_type if self.compiler else None
        extra = self._c_opts.get(compiler_type, [])
        try:
            import pybind11
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise RuntimeError("pybind11 must be installed to build extensions") from exc

        include_dirs = [pybind11.get_include(), pybind11.get_include(user=True)]
        for ext in self.extensions:
            ext.extra_compile_args = list(ext.extra_compile_args or [])
            for flag in extra:
                if flag not in ext.extra_compile_args:
                    ext.extra_compile_args.append(flag)
            ext.include_dirs = list(ext.include_dirs or [])
            for inc in include_dirs:
                if inc not in ext.include_dirs:
                    ext.include_dirs.append(inc)
        super().build_extensions()


class BuildPy(build_py):
    """Regenerate bindings when packaging pure Python sources."""

    def run(self) -> None:
        _generate_bindings()
        super().run()
        _copy_headers(Path(self.build_lib))


class SDist(sdist):
    """Include freshly generated bindings in source distributions."""

    def run(self) -> None:
        _generate_bindings()
        super().run()
