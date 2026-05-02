# pylint: disable=invalid-name
"""
Integration routines for solving the N-Body problem.
Includes SciPy wrappers and a custom Symplectic Velocity-Verlet engine.
"""

from .physics import compute_accelerations

import numpy as np
from scipy.integrate import solve_ivp


def run_simulation(
    physics_func, t_span, y0, masses, G=1.0, rtol=1e-9, atol=1e-12, t_eval=None
):
    """
    Wrapper for Scipy's adaptive integrator.

    Tolerances (rtol, atol) are set high to ensure energy conservation in chaotic orbits.
    """
    sol = solve_ivp(
        fun=physics_func,
        t_span=t_span,
        y0=y0,
        method="RK45",
        args=(masses, G),
        rtol=rtol,
        atol=atol,
        dense_output=True,
        t_eval=t_eval,
    )
    return sol


def verlet_step(state, masses, dt, G=1.0):
    """Advances the simulation by a single time step dt."""
    pos = state[:6]
    vel = state[6:]

    # 1. Current acceleration (Passed G)
    a_current = compute_accelerations(pos, masses, G)

    # 2. Half-step velocity
    v_half = vel + 0.5 * a_current * dt

    # 3. Full-step position
    pos_new = pos + v_half * dt

    # 4. New acceleration (Passed G)
    a_new = compute_accelerations(pos_new, masses, G)

    # 5. Full-step velocity
    v_new = v_half + 0.5 * a_new * dt

    # Package back into a flat 12-element state vector
    new_state = np.zeros(12)
    new_state[:6] = pos_new
    new_state[6:] = v_new

    return new_state


def run_verlet_simulation(y0, masses, t_span, dt, G=1.0):
    """
    Runs a full N-body simulation using the Symplectic Velocity-Verlet engine.
    Acts as a wrapper around verlet_step.
    """
    t_start, t_end = t_span
    times = np.arange(t_start, t_end, dt)
    n_steps = len(times)

    # Pre-allocate states array: (12 rows, n_steps columns)
    states = np.zeros((12, n_steps))
    states[:, 0] = y0

    # The Loop: Just call your single-step function!
    for i in range(n_steps - 1):
        states[:, i + 1] = verlet_step(states[:, i], masses, dt, G)

    return times, states
