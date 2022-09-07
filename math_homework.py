from math import *

a = [-0.1,-0.01,-0.001,0.001,0.01,0.1]

for x in a:
    res = "{:.6f}".format((cos(2*x) - cos(x))/x**2)
    print(res)