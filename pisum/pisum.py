#!/usr/bin/env python
import platform
import timeit
from argparse import ArgumentParser
import math


def pisum_c(N: int) -> float:
    """
    Machin formula for Pi http://mathworld.wolfram.com/PiFormulas.html
    """
    s = 0.0
    for k in range(1, N + 1):
        s += (-1) ** (k + 1) / (2 * k - 1)
    return 4.0 * s


def main():
    p = ArgumentParser(description="pisum benchmark")
    p.add_argument("N", nargs="?", default=1000000, type=int)
    p.add_argument("Nrun", nargs="?", default=10, type=int)
    p = p.parse_args()

    if not math.isclose(math.pi, pisum_c(p.N), rel_tol=1e-4):
        raise SystemExit("CPython convergence error")

    print("--> Python", platform.python_version(), "N=", p.N)
    t = timeit.repeat(
        f"pisum_c({p.N})",
        "import gc; gc.enable(); from __main__ import pisum_c",
        repeat=p.Nrun,
        number=1,
    )

    t = min(t)
    print(f"{t:.3e} seconds.")


if __name__ == "__main__":
    main()
