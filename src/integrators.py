from src import compute_accelerations

import numpy as np
from scipy.integrate import solve_ivp

def run_simulation(physics_func, t_span, y0, masses, G=1.0, rtol=1e-9, atol=1e-12, t_eval=None):
    """
    Wrapper for Scipy's adaptive integrator.
    
    Tolerances (rtol, atol) are set high to ensure energy conservation in chaotic orbits.
    """
    sol = solve_ivp(
        fun=physics_func,
        t_span=t_span,
        y0=y0,
        method='RK45',
        args=(masses, G),
        rtol=rtol,
        atol=atol,
        dense_output=True,
        t_eval=t_eval  

        )
    return sol

def run_verlet_simulation(y0, masses, t_span, dt, G=1.0):
    """Custom Velocity-Verlet engine for long-term energy stability."""
    t_start, t_end = t_span
    times = np.arange(t_start, t_end, dt)
    n_steps = len(times)

    states = np.zeros((12, n_steps))
    states[:, 0] = y0

    for i in range(n_steps - 1):
        curr_y = states[:, i]
        pos, vel = curr_y[:6], curr_y[6:]

        # Half-step velocity
        a_t = compute_accelerations(pos, masses, G)
        v_half = vel + 0.5 * a_t * dt

        # Full-step position
        p_next = pos + v_half * dt

        # Final half-step velocity (using acceleration at new position)
        a_next = compute_accelerations(p_next, masses, G)
        v_next = v_half + 0.5 * a_next * dt

        states[:, i+1] = np.concatenate([p_next, v_next])
    return times, states 