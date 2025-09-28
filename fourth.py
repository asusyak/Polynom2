import numpy as np
import bertini
from bertini import container
from bertini import tracking
from bertini import endgame
from bertini import parse

# from bertini._pybertini.tracking.observers.amp import AMPObserver

from bertini import logging

from bertini.container import ListOfVectorComplexDoublePrecision
from bertini.multiprec import Complex as mpcomplex

tracker_config = tracking.config.AMPConfig
tracker_observer =  tracking.observers.amp


endgame_config = endgame.AMPCauchyEG

logging.init()
logging.set_level(logging.severity_level.Debug)

# bertini.multiprec.Complex

# bertini.function_tree.symbol.make_pi()
# bertini.function_tree.root.

sysNew = bertini.system.System()
sysStart = bertini.system.start_system
totalDegree = bertini.system.start_system.TotalDegree

# Create variables once
x = bertini.function_tree.symbol.Variable("x")
y = bertini.function_tree.symbol.Variable("y")

# Create variable group once
var_group = bertini.VariableGroup()
var_group.append(x)
var_group.append(y)

# Create main system
sys = bertini.System()
sys.add_variable_group(var_group)
sys.add_function(x**2 + y**2 - 1)
sys.add_function(x + y - bertini.multiprec.Complex("0.1234567890123456789"))


# Create start system with same variables and number of functions
start_sys = bertini.System()
start_sys.add_variable_group(var_group)
start_sys.add_function(x - bertini.multiprec.Complex(1))  # Linear start system
start_sys.add_function(y - bertini.multiprec.Complex(0))

# Define homotopy
t = bertini.function_tree.symbol.Variable("t")
homotopy = (1 - t) * sys + t * start_sys
homotopy.add_path_variable(t)

# Create a tracker, for example using DoublePrecisionTracker
tracker = bertini.tracking.DoublePrecisionTracker(homotopy)
tracker1 = bertini.tracking.AMPTracker(homotopy)

# print(dir(tracker))
tracker.tracking_tolerance(1e-12)  # Set a suitable tolerance

tracker1.add_observer(tracker_observer)

# Initial point: use the start system's first start point
# start_point = ListOfVectorComplexDoublePrecision()
# start_point = [mpcomplex("1.0"), mpcomplex("0.0")]

start_point = ListOfVectorComplexDoublePrecision()
#start_point[0] = complex(1.0, 0.0)
#start_point[1] = complex(0.0, 0.0)

#start_point_np = np.array(
#    [complex(z.real, z.imag) for z in start_point],
#    dtype=np.complex128
#)

# Prepare a vector to hold the solution
result = ListOfVectorComplexDoublePrecision()
# result_np = np.zeros(start_point_np.shape, dtype=np.complex128)

start_time = complex(0, 0)
end_time = complex(0, 0)

# Use the Python list of multiprec. Complex as a solution vector
# result = [mpcomplex("0.0") for _ in range(len(var_group))]

# Tracking path from start system (t=1) to target system (t=0)
try:
    # tracker.track_path(result, start_time, end_time, start_point)
    tracker.track_path(result)
    print("Track path succeeded")
except Exception as e:
    print("Python error:", e)

print("Solution:")
for i, val in enumerate(result):
    print(f"x[{i}] = {val}")

# Optionally verify by evaluating polynomials at solution values
#val_f1 = result[0]**2 + result[1]**2 - bertini.multiprec.Complex("1")
#val_f2 = result[0] + result[1] - bertini.multiprec.Complex("0.1234567890123456789")

#print(f"f1 evaluated at solution: {val_f1}")
#print(f"f2 evaluated at solution: {val_f2}")
