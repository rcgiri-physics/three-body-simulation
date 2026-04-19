# Chaotic 3-Body Dynamics: Orbital Stability

A computational study on the gravitational interaction of three point-masses in a 2D plane.

## Research Objectives

1. Model the chaotic trajectories of a 3-body system using a 12-variable state-space.
2. Compare the long-term energy conservation of **Runge-Kutta 4 (RK4)** vs. **Velocity-Verlet (Symplectic)** integration.
3. Visualize stable periodic orbits (e.g., the "Figure-Eight") vs. total system collapse/ejection.

## Methodology

- **Physics:** Newtonian Gravity with Dimensionless Units ($G=1$).
- **Architecture:** Vectorized NumPy engine with decoupled integration and physics logic.
- **Validation:** Monitoring the Hamiltonian (Total Energy) and Angular Momentum conservation.
