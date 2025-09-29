import bertini as pb

pb.logging.init()
# pb.logging.add_file('asdf.txt')

import numpy as np

x = pb.Variable('x')
y = pb.Variable('y')
z = pb.Variable('z')

t = pb.Variable('t')

vg = pb.VariableGroup([x,y,z])

f = pb.System()

f.add_function(x-y)
f.add_function(x**2 + y**2 - 1)
f.add_function(5*x**3 + 16*x*y**4 - 17*x*y*z - z**3)

f.add_variable_group(vg)

g = pb.system.start_system.TotalDegree(f)

#gg = pb.system.start_system.AbstractStartSystem
#q = gg.__class__

#print(q)

homotopy = t*g + (1-t)*f

homotopy.add_path_variable(t);

print('------- homotopy -------')
print(homotopy)

C = pb.multiprec.Complex

tracker = pb.tracking.AMPTracker(homotopy);

print('------- tracker -------')
print(tracker)

result = np.empty((3,),dtype=C)  # right now, if i don't preset to the correct size, i get abort traps.
# there's something deeper wrong with the wrapper i wrote, cuz it should allow resizing, but it's not.

print('------- result before -------')
print(result)

start_point = g.start_point_mp(0)

print('------- start_point -------')
print(start_point)

tracker.track_path(result, C(1) , C(0), start_point)

print('------- result after -------')
print(result)