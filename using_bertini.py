import bertini as pb
import numpy as np

#x = pb.Variable('x')
#y = pb.Variable('y')

current_prec = pb.default_precision()
print(f"Current precision: {current_prec} bits")

tr1 = pb.tracking.DoublePrecisionTracker
tr2 = pb.tracking.MultiplePrecisionTracker
tr3 = pb.tracking.AMPTracker
print(f"Current precision1: {current_prec1} bits")


# Work with multiprecision types
# Create multiprecision complex numbers
z = pb.multiprec.Complex(1.23456789)
print(z)

# Use multiprecision vectors
vec = pb.multiprec.Vector()
print(vec)

# Use adaptive tracker for high precision
#tr = pb.tracking.AMPTracker("homotopy")
#tr.set_tolerance(1e-50)  # Very tight tolerance

z = pb.Variable('z')

#vg = pb.VariableGroup([x,y])
vg1 = pb.VariableGroup([z])

#sys = pb.System()
sys1 = pb.System()

#sys.add_function(x-y)
# sys.add_function(x**2 - 5*x + 6)
#sys.add_function(x**2 + y**2 - 1)
sys1.add_function(z**2 - 5*z + 6)

#sys.add_variable_group(vg)
sys1.add_variable_group(vg1)

C = pb.multiprec.Complex
print(dir(pb))
'''
['System', 'Variable', 'VariableGroup', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', 
'__name__', '__package__', '__path__', '__spec__', '__version__', '__version_info__', '_pybertini', '_version', 
'container', 'default_precision', 'endgame', 'function_tree', 'logging', 'multiprec', 'nag_algorithm', 'parse', 
'random', 'system', 'tracking', 'version']
'''

#variable_values = np.array([C(0), C(0)])
variable_values1 = np.array([C(4)])
# variable_values = np.array([C(0)])

#result = sys.eval(variable_values)
result1 = sys1.eval(variable_values1)
print('-------------- result --------------')
#print('1:', result)
print('2:', result1)

#sys.homogenize()
#sys.auto_patch()

sys1.homogenize()
sys1.auto_patch()

# print(dir(bertini._pybertini.nag_algorithms))
#solver = pb.nag_algorithm.ZeroDimCauchyAdaptivePrecisionTotalDegree(sys)
solver1 = pb.nag_algorithm.ZeroDimPowerSeriesAdaptivePrecisionTotalDegree(sys1)

#solver.solve()
solver1.solve()

print(dir(pb))
'''
['System', 'Variable', 'VariableGroup', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', 
'__name__', '__package__', '__path__', '__spec__', '__version__', '__version_info__', '_pybertini', '_version', 
'container', 'default_precision', 'endgame', 'function_tree', 'logging', 'multiprec', 'nag_algorithm', 'parse', 
'random', 'system', 'tracking', 'version']
'''
print(dir(pb.default_precision))
'''
['__call__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
'__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__name__', 
'__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__setattr__', '__sizeof__',
'__str__', '__subclasshook__', '__text_signature__']
'''
print(dir(pb.nag_algorithm))
'''
['AutoRetrackConfig', 'MidPathConfig', 'PostProcessingConfig', 'RegenerationConfig', 'SharpeningConfig', 
'TolerancesConfig', 'ZeroDimCauchyAdaptivePrecisionTotalDegree', 'ZeroDimCauchyDoublePrecisionTotalDegree', 
'ZeroDimCauchyFixedMultiplePrecisionTotalDegree', 'ZeroDimConfigDoublePrec', 'ZeroDimConfigMultiprec', 
'ZeroDimPowerSeriesAdaptivePrecisionTotalDegree', 'ZeroDimPowerSeriesDoublePrecisionTotalDegree', 
'ZeroDimPowerSeriesFixedMultiplePrecisionTotalDegree', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', 
'__loader__', '__name__', '__package__', '__path__', '__spec__', 'bertini']
'''
#print(dir(solver))
''' solver
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
'__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__instance_size__', '__le__', '__lt__', 
'__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', 
'__subclasshook__', '__weakref__', 'endgame_boundary_data', 'get_endgame', 'get_tracker', 'solution_metadata', 
'solutions', 'solve']
'''
#print(dir(sys))
'''
['__add__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
'__getattribute__', '__getstate__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', 
'__instance_size__', '__le__', '__lt__', '__module__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', 
'__repr__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'add_function', 
'add_functions', 'add_hom_variable_group', 'add_path_variable', 'add_variable_group', 'auto_patch', 'clear_variables', 
'copy_patches', 'copy_variable_structure', 'degrees', 'dehomogenize_point', 'differentiate', 'eval', 'eval_jacobian', 
'function', 'get_patch', 'have_path_variable', 'hom_variable_groups', 'homogenize', 'is_homogeneous', 'is_patched', 
'is_polynomial', 'num_functions', 'num_hom_variable_groups', 'num_hom_variables', 'num_ungrouped_variables', 
'num_variable_groups', 'num_variables', 'precision', 'reorder_functions_by_degree_decreasing', 
'reorder_functions_by_degree_increasing', 'rescale_point_to_fit_patch', 'rescale_point_to_fit_patch_in_place', 
'set_path_variable', 'set_variables', 'variable_groups']
'''

#for soln in solver.solutions():
#    print('-------------- solution --------------')
#    print(sys.dehomogenize_point(soln))

for soln in solver1.solutions():
    print('-------------- solution1 --------------')
    print(sys1.dehomogenize_point(soln))
