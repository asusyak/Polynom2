import os
julia_bin = "/System/Volumes/Data/Users/andriy/Downloads/julia/usr/bin"
os.environ["JULIA_BINDIR"] = julia_bin
os.environ["PATH"] = julia_bin + os.pathsep + os.environ.get("PATH", "")

import julia
from julia import Main

import subprocess
print(subprocess.run(["julia", "--version"], capture_output=True, text=True))

Main.eval("""
using HomotopyContinuation
using DynamicPolynomials

@polyvar x y

F = System([x^2 + 2y - 1,
            y^2 - 2x + 3])

result = solve(F)
""")

solutions = Main.eval("[pr.solution for pr in result]")

print("Solutions found:")
for sol in solutions:
    print(tuple(sol))
