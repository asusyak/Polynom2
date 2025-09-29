import bertini

# this is the target system
sys = bertini.System()
x = bertini.function_tree.symbol.Variable("x") #yes, you can make a variable not match its name...
f = x**3 - 8
sys.add_function(f)

grp = bertini.VariableGroup()
grp.append(x)
sys.add_variable_group(grp)


td = bertini.system.start_system.TotalDegree(sys)
#td.start_point_mp(1)
#td.start_point_d(2)

t = bertini.function_tree.symbol.Variable("t")
homotopy = (1-t)*sys + t*td
homotopy.add_path_variable(t)

tr = bertini.tracking.AMPTracker(homotopy)
tr.tracking_tolerance(1e-5) # track the path to 5 digits or so
# tr.infinite_truncation_tolerance(1e5)

eg = bertini.endgame.AMPCauchyEG(tr)

#stepping = bertini.tracking.config.SteppingConfig()
#stepping.max_step_size = bertini.multiprec.Rational(1,13)
#stepping.

g = bertini.tracking.observers.amp.GoryDetailLogger()
tr.add_observer(g)

# tr.predictor(bertini.tracking.Predictor.RK4)

# stepping.max_step_size = bertini.multiprec.rational(1,13)
results = []

for ii in range(td.num_start_points()):
    results.append(bertini.multiprec.Vector())
    aa = bertini.multiprec.Vector()
    print(">>>")
    print(td.start_point_mp(ii))
    print(td.start_point_d(ii))
    # tr.track_path(result=results[ii],
    tr.track_path(result=results[-1],
                  start_time=bertini.multiprec.Complex(1),
                  end_time=bertini.multiprec.Complex(0),
                  start_point=td.start_point_mp(ii))
    print("***************")
    print(aa)
    print(td.num_start_points())
    print(ii)
    print(results[ii])
    print(results[-1])
    print("***************")

tr.remove_observer(g)

for i, arr in enumerate(results):
    print(f"Array {i}: {arr.tolist()}")