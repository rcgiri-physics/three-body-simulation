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

**Status**: Day 3 - Advanced Integration
**Focus**: Implementing SciPy's solve_ivp for adaptive time-stepping.

### Accomplishments:

- Library Integration: Integrated `scipy.integrate.solve_ivp` as the primary solver.

- Stability Control: Configured the RK45 method with high-precision tolerances ($rtol=10^{-9}$, $atol=10^{-12}$).

### Technical Decision:

While manual fixed-step integrators are educational, they are prone to "energy leakage" during close stellar encounters. By using an adaptive RK45 algorithm, the simulation can dynamically shrink the time step when the potential energy gradient is high, ensuring physical reality is maintained even in chaotic regimes.

## April 22, 2026
**Status:** Day 4 - First Visual Results
**Focus:** Scripting the simulation and verifying the model with known periodic orbits.

### Accomplishments:
* **Automation:** Created `scripts/run_simulation.py` to decouple the laboratory execution from the core physics engine in `src/`.
* **Verification:** Successfully simulated the Chenciner-Montgomery Figure-Eight orbit using high-precision initial conditions.
* **Visualization:** Generated a trajectory plot using Matplotlib, confirming that the three bodies follow the same spatial locus with a relative time delay of $T/3$.

### Technical Observations

The Figure-Eight is a zero-angular-momentum solution. While it looks like a single green curve, it actually represents the paths of all three bodies overlaid. The symmetry of the loops and the sharpness of the central crossing point confirm that the `solve_ivp` adaptive integrator (RK45) is handling the potential energy gradients correctly. Using a relative tolerance of $10^{-9}$ was sufficient to keep the orbit periodic for 5 time units without visible drift.

### Image Analysis (figure_eight.png):

* **Locus:** All three bodies share the same path.
* **Symmetry:** The crossing point is exactly at $(0,0)$.
* **Stability:** The lines overlap perfectly over multiple cycles, indicating minimal numerical dissipation (energy loss).

### Next Step:
Quantify the "Numerical Health" of the system by implementing an Energy Conservation (Hamiltonian) check.