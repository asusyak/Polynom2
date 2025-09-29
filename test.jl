using HomotopyContinuation

@polyvar x

G = (x - 1)*(x - 2)*(x + 3)*(x + 4)*(x - 5)
# F = x^5 - 2x^4 + 3x^3 - 2x^2 + x + 7
F = (x-1.5)*(x-2.5)*(x-3.5)*(x - 1im)*(x+ 1.5 - 2im)

start_system = System([G])
target_system = System([F])

# Solve the start system directly
# start_result = solve(start_system)
start_solutions = [[1.0], [2.0], [-3.0], [-4.0], [5.0]]

# Prepare homotopy and start solutions
H = StraightLineHomotopy(start_system, target_system)

# start_solutions = solutions(start_result)

# Solve homotopy tracking from start_solutions
result = solve(H, start_solutions; show_progress=true, show_warnings=true, tracker_options=TrackerOptions(max_steps=10000))

solutions(result)