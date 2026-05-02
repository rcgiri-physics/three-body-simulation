"""
Module for running a sensitivity sweep on the Figure-Eight orbit.
Gradually increases velocity perturbation to find the ejection threshold.
"""

import os

os.makedirs("plots", exist_ok=True)

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
# Use python -m scripts.run_sensitivity_sweep to run file direcltly from root

import numpy as np
from src.integrators import verlet_step
from src.physics import check_ejection


def run_sweep():
    """
    Executes the parameter sweep over a range of velocity perturbations.
    Prints the survival time for each perturbation to the terminal.
    """
    # Figure-Eight Initial Conditions
    x0 = 0.97000436
    y0 = -0.24308753
    vx0 = -0.4662036850
    vy0 = -0.4323657300
    masses = np.array([1.0, 1.0, 1.0])

    # Nudges to test
    # perturbations = [1e-4, 1e-3, 1e-2, 0.05, 0.1]
    # Nudges to test (We are pushing the velocity by 50% to 200% now!)
    perturbations = [0.1, 0.3, 0.5, 1.0, 2.0]

    dt = 0.01
    max_time = 500.0

    print("Starting Ejection Sensitivity Sweep...")
    print("-" * 40)

    for delta in perturbations:
        # Initial State: Apply the nudge to Body 3's X-velocity
        state = np.array(
            [x0, y0, -x0, -y0, 0.0, 0.0, vx0, vy0, vx0, vy0, -2 * vx0 + delta, -2 * vy0]
        )

        t = 0
        ejected = False

        # Run the simulation loop
        while t < max_time:
            # Take one single step
            state = verlet_step(state, masses, dt)
            t += dt

            # Check for ejection every few steps
            if int(t / dt) % 10 == 0:
                if check_ejection(state, threshold=20.0):
                    ejected = True
                    break

        if ejected:
            print(f"Perturbation {delta:6.4f} -> SYSTEM COLLAPSE at t = {t:.2f}")
        else:
            print(f"Perturbation {delta:6.4f} -> Stable (Survived past t={max_time})")


if __name__ == "__main__":
    run_sweep()
