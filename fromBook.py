import numpy as np
import bertini as pb

pb.logging.init()
# pb.logging.add_file('output.txt')

x = pb.function_tree.symbol.Variable("x")
t = pb.function_tree.symbol.Variable("t")

# this is the target system
target_sys = pb.System()
target_sys.add_function(x**3 - 16)

grp = pb.VariableGroup()
grp.append(x)
target_sys.add_variable_group(grp)

# bertini.nag_algorithm.
# td = bertini.system.start_system.TotalDegree(sys)
#td.start_point_mp(1)
#td.start_point_d(2)

td = pb.System()
td.add_function(x**3 - 8)

grp1 = pb.VariableGroup()
grp1.append(x)
td.add_variable_group(grp1)

start_solutions = [pb.multiprec.Complex(2, 0),
                   pb.multiprec.Complex(-1, 1.73205081),
                   pb.multiprec.Complex(-1, -1.73205081)]

homotopy = (1-t)*target_sys + t*td
homotopy.add_path_variable(t)

tr = pb.tracking.AMPTracker(homotopy)
config_stepping = pb.tracking.config.SteppingConfig();
config_newton = pb.tracking.config.NewtonConfig();
tr.setup(pb.tracking.Predictor.RK4, 1e-5, 1e5, config_stepping, config_newton)

# bertini.tracking.config.

# tr.tracking_tolerance(1e-5) # track the path to 5 digits or so
# tr.infinite_truncation_tolerance(1e5)

eg = pb.endgame.AMPCauchyEG(tr)

#stepping = bertini.tracking.config.SteppingConfig()
#stepping.max_step_size = bertini.multiprec.Rational(1,13)
#stepping.

g = pb.tracking.observers.amp.GoryDetailLogger()
tr.add_observer(g)

# tr.predictor(bertini.tracking.Predictor.RK4)

# stepping.max_step_size = bertini.multiprec.rational(1,13)
results = []
result = np.zeros(dtype=pb.multiprec.Complex, shape=(3))

g1 = pb.system.start_system.TotalDegree(target_sys)
start_point1 = g1.start_point_mp(0)
start_point2 = g1.start_point_mp(1)
start_point3 = g1.start_point_mp(2)
start_point4 = g1.start_point_mp(3)

print(start_point1)
print(start_point2)
print(start_point3)
print(start_point4)

print(start_solutions)
print(start_solutions[0])

# tr.track_path(result, pb.multiprec.Complex(1), pb.multiprec.Complex(0), start_point1)
for sol in start_solutions:
    # tr.track_path(result, pb.multiprec.Complex(1), pb.multiprec.Complex(0), start_point1)
    tr.track_path(result, pb.multiprec.Complex(1), pb.multiprec.Complex(0), sol)

'''
for sol in start_solutions:
    bdry_pt = np.zeros(dtype=pb.multiprec.Complex, shape=(3))
    # bdry_pt = np.zeros(dtype=pb.multiprec.Complex, shape=(1,))
    print(bdry_pt)
    print(sol)
    print(sol.shape)
    tr.track_path(bdry_pt, pb.multiprec.Complex(1), pb.multiprec.Complex(0), sol)
    #results.append(results)

print("Final solutions:")
for s in results:
    print(s)

# for ii in range(td.num_start_points()):
for ii in range(td.num_functions()):
    results.append(bertini.multiprec.Vector())
    aa = bertini.multiprec.Vector()
    print(">>>")
    #print(td.start_point_mp(ii))
    #print(td.start_point_d(ii))
    # tr.track_path(result=results[ii],
    tr.track_path(result=results[-1],
                  start_time=bertini.multiprec.Complex(1),
                  end_time=bertini.multiprec.Complex(0),
                  start_point=td.start_point_mp(ii))
    print("***************")
    print(aa)
    #print(td.num_start_points())
    print(ii)
    print(results[ii])
    print(results[-1])
    print("***************")
'''

tr.remove_observer(g)
