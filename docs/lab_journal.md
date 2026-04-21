# Research Journal: Chaotic 3-Body Dynamics

## April 19, 2026

**Status:** Day 1 - The Setup

Today was mostly about getting the house in order before the real math starts. I set up a professional folder structure (`src`, `docs`, `data`, etc.) to keep things clean from the start.

### What I did

* **The Repo:** Set up a deep `.gitignore` so I don't accidentally upload giant data files later.

* **The Math:** Sat down and mapped out the "State Vector." For 3 bodies in a 2D plane, I'm going to need to track 12 variables (position and velocity for each).

* **The Logic:** Decided to use **Dimensionless Units** ($G=1$). It makes the equations much cleaner and avoids those tiny decimals that usually crash simulations.

### Key Insight (1)

I realized that using the vector form $\mathbf{a} = G m \frac{\mathbf{r}}{r^3}$ is much easier to code than trying to calculate angles with sine and cosine. It handles the direction automatically.

## April 20, 2026

**Status:** Day 2 - Building the Engine
**Focus:** Implementing the ODE Right-Hand Side (RHS)

### Accomplishments

* Created `src/physics.py` with a vectorized `get_derivatives` function.
* Utilized NumPy's `.reshape()` to transform the flat 12-variable state vector into a readable (3, 2) coordinate matrix during calculation.
* Implemented the $1/r^3$ gravitational force vector logic, ensuring that self-interaction ($i=j$) is excluded to avoid singularities.

### Key Insight (2)

Reshaping the state vector within the derivative function allows for "Human-Readable Math" while maintaining "Computer-Readable Structure" for the integrator. It bridges the gap between 2D physical space and 1D state space.

### Next Step

Set up the `integrators.py` file to include the RK4 stepper.


## April 21, 2026

### Strategy: Decided to utilize `scipy.integrate.solve_ivp` directly.

Reasoning: Manual fixed-step integrators are prone to "energy leakage" and failure during close approaches in N-body systems. By using RK45 with adaptive stepping, I can ensure the simulation maintains a high degree of energy conservation even as the system approaches chaos.