"""
Calculating the maximum taper angle possible to satisfy design requirements.
"""
import math
import numpy as np
import matplotlib.pyplot as plt

### Material Properties ###
E = 210E9
v = 0.3
dens = 7850

### Predetermined bracket dimensions ###
L = 8
h0 = 0.3
t = 0.3
min_delta = 1.5333 #minimum taper angle to maintain 8m length and 0.3m h0 
max_delta = 90 * (math.pi / 180)

### Design Requirements ###
max_def = 0.001
SF = 2.5 #safety factor
g = 9.81
heli_weight = 0.7E3 * g
heli_weight_sf = heli_weight*SF 

def plot_load_theta():
    theta = np.linspace(min_delta,max_delta,100)
    h1 = np.linspace (0,0.3,100)
    w_plot = []
    volume_plot = []
    for num in h1:
        # w = (max_def * E * L**2 * np.tan(np.radians(num))**2) / (4 * h0**2)
        w = (max_def * (h0**3) * (1-(h1/h0))**2)/(4*(L**4))
        w_plot.append(w)

    plt.plot(h1,w)
    plt.show()

plot_load_theta()