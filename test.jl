using HomotopyContinuation

@polyvar x

G = (x - 1)*(x - 2)*(x + 3)*(x + 4)*(x - 5)
F = x^5 + 2x^4 - x + 7

start_system = System([G])
target_system = System([F])

# Solve the start system directly
start_result = solve(start_system)

# Prepare homotopy and start solutions
H = StraightLineHomotopy(start_system, target_system)
start_solutions = solutions(start_result)

# Solve homotopy tracking from start_solutions
result = solve(H, start_solutions)
