from __future__ import annotations
import subprocess
import sys
import shutil
import os
from pathlib import Path

R = Path(__file__).parent / "build"


def compiler_info() -> dict[str, str]:
    """
    assumes CMake project has been generated
    """

    fn = R / "CMakeCache.txt"

    if not fn.is_file():
        print("Must build Fortran / C code via CMake", file=sys.stderr)
        return {"cc": "", "fc": "", "ccvers": "", "fcvers": ""}

    cc = ""
    fc = ""
    for ln in fn.open("r"):
        if ln.startswith("CMAKE_C_COMPILER:"):
            cc = ln.split("/")[-1].rstrip().replace(".exe", "")
        elif ln.startswith("CMAKE_Fortran_COMPILER:"):
            fc = ln.split("/")[-1].rstrip().replace(".exe", "")

    if cc == "cc":
        cc = "gcc"

    # %% versions
    cvers = fvers = ""
    try:
        match cc:
            case "clang":
                cvers = subprocess.check_output([cc, "-dumpversion"], text=True).rstrip()
            case "gcc":
                ret = subprocess.check_output([cc, "--version"], text=True).split("\n")
                cvers = ret[0].split()[-1]
            case "icx":
                ret = subprocess.check_output([cc, "--version"], text=True).split("\n")
                cvers = ret[0].split()[-2][:4]
            case "nvcc":
                ret = subprocess.check_output([cc, "--version"], text=True).split("\n")
                cvers = ret[1].split()[1][:5]

        match fc:
            case "flang":
                fvers = subprocess.check_output([fc, "-dumpversion"], text=True).rstrip()
            case "gfortran":
                ret = subprocess.check_output([fc, "--version"], text=True).split("\n")
                fvers = ret[0].split()[-1]
            case "ifx":
                ret = subprocess.check_output([fc, "--version"], text=True).split("\n")
                fvers = ret[0].split()[-2][:4]
            case "nvfortran":
                ret = subprocess.check_output([fc, "--version"], text=True).split("\n")
                fvers = ret[1].split()[1][:5]

    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    cinf = {"cc": cc, "ccvers": cvers, "fc": fc, "fcvers": fvers}

    return cinf


def run(cmd: list[str | None], bdir: Path, lang: str | None = None) -> tuple[float, str]:
    if cmd[0] is None:
        raise EnvironmentError(f"{lang}: MISSING")

    if not lang:
        lang = cmd[0]

    path = None
    exe = None
    if cmd[0] == "octave-cli":
        if hint := os.getenv("OCTAVE_EXECUTABLE"):
            path = Path(hint).parent
        if path:
            exe = shutil.which(cmd[0], path=path)
    if cmd[0] == "matlab":
        if hint := os.getenv("Matlab_ROOT"):
            path = Path(hint) / "bin"
        if path:
            exe = shutil.which(cmd[0], path=path)
    if not exe:
        exe = shutil.which(cmd[0])
    if exe is None:
        raise EnvironmentError(f"{lang}: MISSING")

    if cmd[0] == "gdl":
        vers = subprocess.check_output(["gdl", "--version"], text=True).split()[-2]
        cmd += ["--fakerelease", vers]

    assert isinstance(exe, str)
    print("-->", lang)
    ret = subprocess.check_output([exe] + cmd[1:], cwd=bdir, text=True).split("\n")  # type: ignore
    # print(ret)
    t = float(ret[-2].split()[0])
    # %% version
    vers = ""
    if cmd[0] in {
        "julia",
        "cython",
        "matlab",
        "numba",
        "python",
        "octave",
        "octave-cli",
        "pypy",
        "pypy3",
    }:
        vers = ret[0].split()[2]
    elif cmd[0] == "idl":
        vers = ret[-3].split()[0]
    elif cmd[0] == "gdl":
        vers = ret[-3].split()[0]

    return t, vers
