import os
os.makedirs('plots', exist_ok=True)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
# Use python -m scripts.energy_analysis to run direltly from root)

import numpy as np
import matplotlib.pyplot as plt
from src import get_derivatives, run_simulation, calculate_energy

# Reuse Figure-Eight ICs from Day 4
masses = np.array([1.0, 1.0, 1.0])
r1, r2, r3 = np.array([-0.97, 0.24]), np.array([0.97, -0.24]), np.array([0.0, 0.0])
v3 = np.array([-0.93240737, -0.86473146])
v1, v2 = -0.5 * v3, -0.5 * v3
y0 = np.concatenate([r1, r2, r3, v1, v2, v3])

# Run for a longer duration to check for drift
sol = run_simulation(get_derivatives, (0, 20), y0, masses)

# Calculate energy at every time step
total_e, kin_e, pot_e = [], [], []
for i in range(len(sol.t)):
    e, k, p = calculate_energy(sol.y[:, i], masses)
    total_e.append(e)
    kin_e.append(k)
    pot_e.append(p)

# Plotting
fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top Plot: Kinetic and Potential (They should dance around each other)
ax[0].plot(sol.t, kin_e, label='Kinetic (T)', color='orange')
ax[0].plot(sol.t, pot_e, label='Potential (V)', color='purple')
ax[0].set_ylabel("Energy")
ax[0].legend()
ax[0].set_title("Energy Partitioning vs. Conservation")

# Bottom Plot: Total Energy (Should be a flat line)
# We plot the deviation from initial energy to see tiny errors
# Using r prefix for Latex labels
e_error = (np.array(total_e) - total_e[0]) / total_e[0]
ax[1].plot(sol.t, e_error, color='black', label='Relative Energy Error')
ax[1].set_ylabel(r"$\Delta E / E_0$")
ax[1].set_xlabel("Time")
ax[1].legend()

plt.tight_layout()
plt.savefig('plots/energy_conservation.png')
plt.show()