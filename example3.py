import bertini as pb

x = pb.Variable('x')

sys = pb.System()
sys.add_function(x**2 + 4)

sys.add_variable_group(pb.VariableGroup([x]))
sys.homogenize()
sys.auto_patch()

solver = pb.nag_algorithm.ZeroDimCauchyAdaptivePrecisionTotalDegree(sys)
solver.solve()
# print(solver.solutions())

for soln in solver.solutions():
    print('--- 1')
    print(soln)
    print('--- 2')
    print(sys.dehomogenize_point(soln))
    print('--- 3')