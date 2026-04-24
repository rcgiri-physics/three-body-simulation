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
t_span = (0, 60)
t_eval = np.linspace(t_span[0], t_span[1], 5000) # 5,000 even points
sol_a = run_simulation(get_derivatives, t_span, y0_control, masses, t_eval=t_eval)
sol_b = run_simulation(get_derivatives, t_span, y0_perturbed, masses, t_eval=t_eval)

# Visualization: The Unzipping Trajectories
plt.figure(figsize=(10, 6))
plt.plot(sol_a.y[0], sol_a.y[1], color='blue', alpha=0.5, label='Control')
plt.plot(sol_b.y[0], sol_b.y[1], color='red', linestyle='--', alpha=0.8, label='Perturbed')
plt.title("Long-Term Divergence: The Death of the Figure-Eight")
plt.legend()
plt.savefig('plots/butterfly_extended.png')

# Visualization: Logarithmic Divergence (Quantitative Chaos)
plt.figure(figsize=(10, 5))
# Ensure we compare the same time points
delta_y = sol_a.y - sol_b.y
separation = np.linalg.norm(delta_y, axis=0)

plt.semilogy(sol_a.t, separation, color='darkred')
plt.title("Growth of Phase-Space Distance (Lyapunov Divergence)")
plt.ylabel(r"Distance ($||\Delta y||$)")
plt.xlabel("Time")
plt.grid(True, which="both", alpha=0.2)
plt.savefig('plots/divergence_plot.png')
plt.show()