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


## April 23, 2026
**Status:** Day 5 - The Energy Audit

**Focus:** Quantifying numerical precision through Hamiltonian conservation.

### Accomplishments:
* **Physics Expansion:** Implemented the `calculate_energy` function, partitioning the system into its Kinetic ($T$) and Potential ($V$) components.
* **Diagnostics:** Created `scripts/energy_analysis.py` to monitor the Hamiltonian over an extended horizon ($t=20$).
* **Verification:** Generated `plots/energy_conservation.png`, proving the simulation's physical validity.

### Technical Observations:
The energy audit confirms that the system is highly conserved. The relative energy error ($\Delta E/E_0$) remains within a magnitude of $10^{-9}$ over the duration of the test. While a slight linear drift is visible—a known artifact of the non-symplectic nature of the RK45 algorithm—the precision is more than sufficient for characterizing stable periodic orbits.

### Image Analysis (energy_conservation.png):

* **Top Panel (Energy Partitioning):** The plot shows the exchange between Kinetic ($T$) and Potential ($V$) energy. As the three bodies reach the narrow "waist" of the figure-eight, their velocities peak (maximum $T$) while their proximity creates a deep gravitational well (minimum $V$). The perfect anti-correlation of these curves is the first sign of a stable numerical solution.
* **Bottom Panel (Relative Error):** The Hamiltonian error ($\Delta E / E_0$) is maintained at a magnitude of $\sim 10^{-9}$. 
* **Drift Observation:** A slight linear downward trend is visible in the error plot. This is a characteristic "feature" of the RK45 integrator; because it is not symplectic, it does not perfectly preserve the area in phase space, leading to a tiny, systematic energy leak. For the current scope, this drift is negligible, but it provides a strong justification for implementing a Velocity-Verlet solver in the next phase.

**Current Status:** The physics engine is now fully validated and verified. The system is computationally stable and ready for experimental perturbation.