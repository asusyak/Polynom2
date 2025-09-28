import os
julia_bin = "/System/Volumes/Data/Users/andriy/Downloads/julia/usr/bin"
os.environ["JULIA_BINDIR"] = julia_bin
os.environ["PATH"] = julia_bin + os.pathsep + os.environ.get("PATH", "")

from julia import Main

import subprocess
print(subprocess.run(["julia", "--version"], capture_output=True, text=True))

Main.eval("""
using HomotopyContinuation
using DynamicPolynomials

@polyvar x 

# p = (1 + 2im)*x^3 + (3 - im)*x^2 + 2im*x + 1
p = x^4 -3*x^3 -2*x^2 + 10*x - 12
F = System([p])

result = solve(F)
""")

solutions = Main.eval("[pr.solution for pr in result]")

print("Solutions found:")
for sol in solutions:
    print(tuple(sol))
