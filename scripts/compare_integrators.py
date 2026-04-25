import os
os.makedirs('plots', exist_ok=True)

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
# Use python -m scripts.compare_integrators to run direltly from root)

import numpy as np
import matplotlib.pyplot as plt
from src import get_derivatives, run_simulation, calculate_energy
from src.integrators import run_verlet_simulation

# Setup Initial Conditions (Figure-Eight)
masses = np.array([1.0, 1.0, 1.0])
y0 = np.array([-0.97000436, 0.24308753, 0.97000436, -0.24308753, 0.0, 0.0,
               0.466203685, 0.43236573, 0.466203685, 0.43236573, -0.93240737, -0.86473146])

t_span = (0, 100)
dt = 0.005 # Small fixed step for Verlet

# Run Both
sol_rk = run_simulation(get_derivatives, t_span, y0, masses)
t_v, sol_v = run_verlet_simulation(y0, masses, t_span, dt)

# Calculate Energy Error Function
def get_errors(t, y):
    energies = [calculate_energy(y[:, i], masses) for i in range(len(t))]
    return np.abs((np.array(energies) - energies[0]) / energies[0])

# Plotting
plt.figure(figsize=(10, 6))
plt.semilogy(sol_rk.t, get_errors(sol_rk.t, sol_rk.y), label='RK45 (Adaptive)')
plt.semilogy(t_v, get_errors(t_v, sol_v), label='Velocity-Verlet (Symplectic)')
plt.title("Energy Stability: RK45 vs. Velocity-Verlet")
plt.ylabel(r"Relative Error $\Delta E/E_0$")
plt.legend()
plt.savefig('plots/integrator_comparison.png')
plt.show()