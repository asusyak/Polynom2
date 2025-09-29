import bertini.system.start_system
import mpmath
from mpmath import mpc
import numpy as np
import bertini as pb
import bertini._pybertini as pybertini

pb.logging.init()
# pb.logging.add_file('output.txt')
# pb.nag_algorithm.

x = pb.function_tree.symbol.Variable("x")
t = pb.function_tree.symbol.Variable("t")

###############################################################################
# this is the target system
###############################################################################
target_sys = pb.System()
target_sys.add_function(x**3 - 16)
grp = pb.VariableGroup()
grp.append(x)
target_sys.add_variable_group(grp)

###############################################################################
# this is the source system
###############################################################################
td = pb.System()
td.add_function(x**3 - 8)
grp1 = pb.VariableGroup()
grp1.append(x)
td.add_variable_group(grp1)
print('------------ degrees')
print(td.degrees())

start_solutions = [(2, 0),
                   (2, 0),
                   (2, 0)]
#start_solutions_fixed = np.array([(2.0 + 1.0j)], dtype=object)
#correct = np.array([(2.0, 0.0)], dtype=object)

dt = np.dtype([('x', 'f8'), ('y', 'f8')])
start_solutions_fixed = np.array([(2.0, 0.0)], dtype=dt)

#start_solutions2 = np.array(start_solutions, dtype=object)

homotopy = (1-t)*target_sys + t*td
homotopy.add_path_variable(t)
print('-------------- homotopy.degrees()')
print(homotopy.degrees())

###############################################################################
# setup tracker
###############################################################################
tracker = pb.tracking.AMPTracker(homotopy)
config_stepping = pb.tracking.config.SteppingConfig()
config_newton = pb.tracking.config.NewtonConfig()
config_amp = pb.tracking.config.AMPConfig(homotopy)
tracker.setup(pb.tracking.Predictor.RK4, 1e-5, 1e5, config_stepping, config_newton)
# tr.tracking_tolerance(1e-5) # track the path to 5 digits or so
# tr.infinite_truncation_tolerance(1e5)

eg = pb.endgame.AMPCauchyEG(tracker)

#stepping.max_step_size = bertini.multiprec.Rational(1,13)

g = pb.tracking.observers.amp.GoryDetailLogger()
tracker.add_observer(g)

results = []
result = np.zeros(dtype=pb.multiprec.Complex, shape=(3))
result1 = np.zeros(dtype=pb.multiprec.Complex, shape=1)
f1 = x**3 - 8
g1 = pb.system.start_system.TotalDegree(target_sys)
g2 = pb.system.start_system.AbstractStartSystem

g2.add_function(f1)
print('>>>>>>>>>>>>>> g1')
print(g1)
print('>>>>>>>>>>>>>> g2')
print(g2)
g2.add_function(f1)
print(g2.num_start_points())
print('>>>>>>>>>>>>>> number of start points')
print(g1.num_start_points())
start_point1 = g1.start_point_mp(0)
#start_point2 = g1.start_point_mp(1)
#start_point3 = g1.start_point_mp(2)
#start_point4 = g1.start_point_mp(3)

print(">>>>>>>>> start_point1")
print(start_point1)
print(type(start_point1))
print(start_point1.__class__)
#print(">>>>>>>>> end start_point1")
#print(start_point2)
#print(start_point3)
#print(start_point4)
#print(start_point1.__class__.__class__)

#print(">>>>>>>>> start_solutions")
#print(start_solutions[0])
#print(start_solutions[0].__class__)
#print(start_solutions2[0].__class__.__class__)

print(">>>>>>>>> start_solutions_fixed")
print(start_solutions_fixed
      )
print(start_solutions_fixed[0])
print(type(start_solutions_fixed))
print(type(start_solutions_fixed[0]))
print(start_solutions_fixed[0].__class__)
#print(start_solutions2[0].__class__.__class__)


# tr.track_path(result, pb.multiprec.Complex(1), pb.multiprec.Complex(0), start_point1)
for sol in start_solutions_fixed:
    # tracker.track_path(result, pb.multiprec.Complex(1), pb.multiprec.Complex(0), start_point1)
    tracker.track_path(result, pb.multiprec.Complex(1), pb.multiprec.Complex(0), start_solutions_fixed)
    print(result)
    print('end result')
    # tr.track_path(result, pb.multiprec.Complex(1), pb.multiprec.Complex(0), start_solutions3[0])
    #tr.track_path(result1, pb.multiprec.Complex(1), pb.multiprec.Complex(0), start_point1[0])

'''
for sol in start_solutions:
    bdry_pt = np.zeros(dtype=pb.multiprec.Complex, shape=(3))
    # bdry_pt = np.zeros(dtype=pb.multiprec.Complex, shape=(1,))
    tr.track_path(bdry_pt, pb.multiprec.Complex(1), pb.multiprec.Complex(0), sol)
    #results.append(results)

print("Final solutions:")
for s in results:
    print(s)

# for ii in range(td.num_start_points()):
for ii in range(td.num_functions()):
    results.append(bertini.multiprec.Vector())
    aa = bertini.multiprec.Vector()
    # tr.track_path(result=results[ii],
    tr.track_path(result=results[-1],
                  start_time=bertini.multiprec.Complex(1),
                  end_time=bertini.multiprec.Complex(0),
                  start_point=td.start_point_mp(ii))
'''

tracker.remove_observer(g)
