import bertini.system.start_system
import mpmath
from mpmath import mpc
import numpy as np
import bertini as pb
import bertini._pybertini as pybertini

pybertini.logging.init()
# pybertini.logging.add_file('output.txt')
# pybertini.nag_algorithm.

x = pybertini.function_tree.symbol.Variable("x")
t = pybertini.function_tree.symbol.Variable("t")

###############################################################################
# this is the target system
###############################################################################
target_sys = pybertini.system.System()
target_sys.add_function(x**3 - 16)
grp = pb.VariableGroup()
grp.append(x)
target_sys.add_variable_group(grp)

###############################################################################
# this is the source system
###############################################################################
td = pybertini.system.start_system.TotalDegree(target_sys)
homotopy = (1-t)*target_sys + t*td
homotopy.add_path_variable(t)
print('-------------- homotopy.degrees()')
print(homotopy.degrees())

###############################################################################
# setup tracker
###############################################################################
tracker = pybertini.tracking.AMPTracker(homotopy)
config_stepping = pybertini.tracking.config.SteppingConfig()
config_newton = pybertini.tracking.config.NewtonConfig()
config_amp = pybertini.tracking.config.AMPConfig(homotopy)
tracker.setup(pybertini.tracking.Predictor.RK4, 1e-5, 1e5, config_stepping, config_newton)
# tr.tracking_tolerance(1e-5) # track the path to 5 digits or so
# tr.infinite_truncation_tolerance(1e5)

#start_solutions = [(2, 0),
#                   (2, 0),
#                   (2, 0)]
#start_solutions_fixed = np.array([(2.0 + 1.0j)], dtype=object)
#correct = np.array([(2.0, 0.0)], dtype=object)

#dt = np.dtype([('x', 'f8'), ('y', 'f8')])
#start_solutions_fixed = np.array([(2.0, 0.0)], dtype=dt)

#start_solutions2 = np.array(start_solutions, dtype=object)



eg = pybertini.endgame.AMPCauchyEG(tracker)

#stepping.max_step_size = bertini.multiprec.Rational(1,13)

g = pybertini.tracking.observers.amp.GoryDetailLogger()
tracker.add_observer(g)

results = []
result = np.zeros(dtype=pybertini.multiprec.Complex, shape=(3))
result1 = np.zeros(dtype=pybertini.multiprec.Complex, shape=1)
f1 = x**3 - 8
# g1 = pybertini.system.start_system.TotalDegree(target_sys)

print('>>>>>>>>>>>>>> number of start points')
#print(td.num_start_points())
start_point1 = td.start_point_mp(0)
#start_point2 = g1.start_point_mp(1)
#start_point3 = g1.start_point_mp(2)
#start_point4 = g1.start_point_mp(3)

# tr.track_path(result, pybertini.multiprec.Complex(1), pybertini.multiprec.Complex(0), start_point1)
for sol in start_solutions_fixed:
    # tracker.track_path(result, pybertini.multiprec.Complex(1), pybertini.multiprec.Complex(0), start_point1)
    tracker.track_path(result,
                       pybertini.multiprec.Complex(1),
                       pybertini.multiprec.Complex(0),
                       start_solutions_fixed)
    print(result)
    print('end result')
    # tr.track_path(result, pybertini.multiprec.Complex(1), pybertini.multiprec.Complex(0), start_solutions3[0])
    #tr.track_path(result1, pybertini.multiprec.Complex(1), pybertini.multiprec.Complex(0), start_point1[0])

'''
for sol in start_solutions:
    bdry_pt = np.zeros(dtype=pybertini.multiprec.Complex, shape=(3))
    # bdry_pt = np.zeros(dtype=pybertini.multiprec.Complex, shape=(1,))
    tr.track_path(bdry_pt, pybertini.multiprec.Complex(1), pybertini.multiprec.Complex(0), sol)
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
