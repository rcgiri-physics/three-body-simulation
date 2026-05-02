# pylint: disable=invalid-name
"""
Simulates the Sun, Earth, and Jupiter using Astronomical Units.
"""

import os
import sys
from pathlib import Path

# Ensure plots directory exists and modules can be imported from root
os.makedirs("plots", exist_ok=True)
sys.path.append(str(Path(__file__).parent.parent))

import numpy as np
import matplotlib.pyplot as plt
from src.integrators import run_verlet_simulation


def run_solar_system():
    """Executes the 12-year solar system simulation and plots the orbits."""
    # 1. The Physics Constants
    G_astro = 4 * (np.pi**2)  # G in AU, Years, and Solar Masses

    # 2. The Masses (Sun, Earth, Jupiter)
    m_sun = 1.0
    m_earth = 3.003e-6  # Earth is tiny compared to the Sun
    m_jupiter = 9.543e-4  # Jupiter is about 1/1000th of the Sun
    masses = np.array([m_sun, m_earth, m_jupiter])

    # 3. Initial Positions (in AU)
    # Sun at center, Earth at 1 AU, Jupiter at 5.2 AU
    pos = np.array([[0.0, 0.0], [1.0, 0.0], [5.2, 0.0]])  # Sun  # Earth  # Jupiter

    # 4. Initial Velocities (in AU / Year)
    # v = sqrt(G * M_sun / r)
    v_earth = np.sqrt(G_astro * m_sun / 1.0)
    v_jupiter = np.sqrt(G_astro * m_sun / 5.2)

    vel = np.array(
        [
            [0.0, 0.0],  # Sun (Mostly stationary)
            [0.0, v_earth],  # Earth moving 'up' (Y-direction)
            [0.0, v_jupiter],  # Jupiter moving 'up' (Y-direction)
        ]
    )

    # Pack into your 12-element state vector format
    state_0 = np.zeros(12)
    state_0[:6] = pos.flatten()
    state_0[6:] = vel.flatten()

    # 5. Run the Engine!
    # Let's run it for 12 years (1 full orbit for Jupiter, 12 for Earth)
    # We need a smaller dt because Earth moves fast (1 year orbit)
    dt = 0.001
    t_max = 12.0

    print("Simulating 12 years of the Solar System...")
    _, history = run_verlet_simulation(
        state_0, masses, t_span=(0, t_max), dt=dt, G=G_astro
    )

    # 6. Plot the Orbits
    pos_data = history[:6, :].T.reshape(-1, 3, 2)

    plt.figure(figsize=(8, 8))
    plt.plot(pos_data[:, 0, 0], pos_data[:, 0, 1], color="yellow", label="Sun", lw=2)
    plt.plot(pos_data[:, 1, 0], pos_data[:, 1, 1], color="blue", label="Earth", lw=1)
    plt.plot(
        pos_data[:, 2, 0], pos_data[:, 2, 1], color="orange", label="Jupiter", lw=1.5
    )

    # Plot starting positions as dots
    plt.scatter(pos_data[0, 0, 0], pos_data[0, 0, 1], color="yellow", s=100, zorder=5)
    plt.scatter(pos_data[0, 1, 0], pos_data[0, 1, 1], color="blue", s=50, zorder=5)
    plt.scatter(pos_data[0, 2, 0], pos_data[0, 2, 1], color="orange", s=80, zorder=5)

    # FIXED: Removed the 'f' prefix from this string
    plt.title("Solar System Simulation (12 Years)\nG = 4π²")
    plt.xlabel("Astronomical Units (AU)")
    plt.ylabel("Astronomical Units (AU)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.axis("equal")

    plt.savefig("plots/solar_system.png")
    print("Saved to plots/solar_system.png!")


if __name__ == "__main__":
    run_solar_system()
