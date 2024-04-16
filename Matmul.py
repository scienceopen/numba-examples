#!/usr/bin/env python
from pathlib import Path
from argparse import ArgumentParser
import typing as T
import shutil
import logging
import platform

import benchmark as pb

try:
    from matplotlib.pyplot import figure
except ImportError:
    figure = None  # type: ignore

bdir = Path(__file__).parent / "matmul"
cdir = Path(__file__).parent / "build" / "matmul"


def main():
    p = ArgumentParser()
    p.add_argument("-N", type=int, default=1000)
    p.add_argument("-Nrun", type=int, default=10)
    p = p.parse_args()

    times = benchmark_matmul(p.N, p.Nrun)
    for k, v in times.items():
        print(k, v)

    if figure is not None and len(times) > 0:
        fg = figure()
        ax = fg.gca()
        ax.scatter(times.keys(), times.values())

        ax.set_title(f"Matmul, N={p.N}    {platform.system()}  {platform.machine()}")
        ax.set_ylabel("run time [sec.]")
        # ax.set_yscale('log')
        ax.grid(True)
        # ax.autoscale(True)  # bug?
        # ax.legend(loc='best')
        figfn = bdir / "matmul.png"
        print("saved figure to", figfn)
        fg.savefig(figfn)


def benchmark_matmul(N: int, Nrun: int) -> T.Dict[str, float]:
    times = {}
    compinf = pb.compiler_info()
    matmul_exe = shutil.which("matmul_fort", path=str(cdir))

    try:
        t = pb.run([matmul_exe, str(N), str(Nrun)], cdir, "fortran")
        times["Fortran\n" + compinf["fc"] + "\n" + compinf["fcvers"]] = t[0]
    except EnvironmentError:
        logging.error("Fortran compiler not found")

    try:
        t = pb.run(["julia", "matmul.jl", str(N)], bdir)
        times["julia \n" + t[1]] = t[0]
    except EnvironmentError:
        logging.error("Julia not found")

    try:
        t = pb.run(["gdl", "-q", "-e", "matmul", "-arg", str(N)], bdir)
        times["gdl \n" + t[1]] = t[0]
    except EnvironmentError:
        logging.error("GDL not found")

    try:
        t = pb.run(["idl", "-quiet", "-e", "matmul", "-arg", str(N)], bdir)
        times["idl \n" + t[1]] = t[0]
    except EnvironmentError:
        logging.error("IDL not found")

    # octave-cli, not octave in general
    try:
        t = pb.run(["octave-cli", "--eval", f"matmul({N},{Nrun})"], bdir)
        times["octave \n" + t[1]] = t[0]
    except EnvironmentError:
        logging.error("Octave not found")

    try:
        t = pb.run(["matlab", "-batch", f"matmul({N},{Nrun})"], bdir)
        times["matlab \n" + t[1]] = t[0]
    except EnvironmentError:
        logging.error("Matlab not found")

    t = pb.run(["python", "matmul.py", str(N), str(Nrun)], bdir)
    times["python \n" + t[1]] = t[0]

    return times


# %%
if __name__ == "__main__":
    main()
