import os
os.makedirs('plots', exist_ok=True)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
# Use python -m scripts.run_simulation to run file direcltly from root

import numpy as np
import matplotlib.pyplot as plt
from src import get_derivatives, run_simulation

# 1. Setup Initial Conditions (Figure-Eight Orbit)
G = 1.0
masses = np.array([1.0, 1.0, 1.0])

# Positions (x, y)
r1 = np.array([-0.97000436, 0.24308753])
r2 = np.array([0.97000436, -0.24308753])
r3 = np.array([0.0, 0.0])

# Velocities (vx, vy)
v3 = np.array([-0.93240737, -0.86473146])
v1 = -0.5 * v3
v2 = -0.5 * v3

# Flatten into a 12-element state vector
y0 = np.concatenate([r1, r2, r3, v1, v2, v3])

# 2. Run the Simulation
t_span = (0, 5) # 5 time units
sol = run_simulation(get_derivatives, t_span, y0, masses, G)

# 3. Visualization
plt.figure(figsize=(8, 8))

# Unpack the results
# sol.y has shape (12, number_of_steps)
x1, y1 = sol.y[0], sol.y[1]
x2, y2 = sol.y[2], sol.y[3]
x3, y3 = sol.y[4], sol.y[5]

plt.plot(x1, y1, label='Body 1', color='red')
plt.plot(x2, y2, label='Body 2', color='blue')
plt.plot(x3, y3, label='Body 3', color='green')

plt.title("The Figure-Eight 3-Body Orbit")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True, linestyle='--')

# Save the result to your plots folder
plt.savefig('plots/figure_eight.png')
plt.show()