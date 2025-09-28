import bertini

x = bertini.function_tree.symbol.Variable("x") #yes, you can make a variable not match its name...
y = bertini.function_tree.symbol.Variable("y")

f = x**2 + y**2 -1
g = x+y

sys = bertini.System()
sys.add_function(f)
sys.add_function(g)

grp = bertini.VariableGroup()
grp.append(x)
grp.append(y)

sys.add_variable_group(grp)
td = bertini.system.start_system.TotalDegree(sys)

t = bertini.function_tree.symbol.Variable("t")
homotopy = (1-t)*sys + t*td
homotopy.add_path_variable(t)
tr = bertini.tracking.AMPTracker(homotopy)
g = bertini.tracking.observers.amp.GoryDetailLogger()
tr.add_observer(g)

tr.tracking_tolerance(1e-5) # track the path to 5 digits or so
tr.infinite_truncation_tolerance(1e5)
# tr.predictor(bertini.tracking.Predictor.RK4)

stepping = bertini.tracking.config.SteppingConfig()
# stepping.max_step_size = bertini.multiprec.rational(1,13)
results = []

for ii in range(td.num_start_points()):
    results.append(bertini.multiprec.Vector())
    tr.track_path(result=results[-1],
                  start_time=bertini.multiprec.Complex(1),
                  end_time=bertini.multiprec.Complex(0),
                  start_point=td.start_point_mp(ii))

tr.remove_observer(g)