import os
os.makedirs('plots', exist_ok=True)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
# Use python -m scripts.energy_analysis to run direltly from root)

import numpy as np
import matplotlib.pyplot as plt
from src import get_derivatives, run_simulation

# Standard Figure-Eight ICs
masses = np.array([1.0, 1.0, 1.0])
r1, r2, r3 = np.array([-0.97000436, 0.24308753]), np.array([0.97000436, -0.24308753]), np.array([0.0, 0.0])
v3 = np.array([-0.93240737, -0.86473146])
v1, v2 = -0.5 * v3, -0.5 * v3

y0_control = np.concatenate([r1, r2, r3, v1, v2, v3])

# Perturbed ICs (The butterfly nudge)
# We add a tiny 0.0001 to the x-velocity of Body 1
y0_perturbed = y0_control.copy()
y0_perturbed[6] += 1e-4

# Run both simulations
t_span = (0, 15)
sol_a = run_simulation(get_derivatives, t_span, y0_control, masses)
sol_b = run_simulation(get_derivatives, t_span, y0_perturbed, masses)

# Plotting the divergence
plt.figure(figsize=(10, 6))

# Plot Body 1 from Control (Solid line)
plt.plot(sol_a.y[0], sol_a.y[1], color='blue', alpha=0.6, label='Control (Body 1)')

# Plot Body 1 from Perturbed (Dashed line)
plt.plot(sol_b.y[0], sol_b.y[1], color='red', linestyle='--', alpha=0.8, label='Perturbed (Body 1)')

plt.title("The butterfly effect: Figure-Eight Sensitivity")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('plots/butterfly_effect.png')