import numpy as np
from scipy.integrate import solve_ivp

def run_simulation(physics_func, t_span, y0, masses, G=1.0, rtol=1e-9, atol=1e-12):
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
        dense_output=True # For smooth plot
        )
    return sol
