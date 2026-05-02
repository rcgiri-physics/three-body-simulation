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

## April 24, 2026
**Status:** Day 6 - Quantitative Chaos & Resynchronization

**Focus:** Measuring the Lyapunov divergence of the Figure-Eight orbit.

### Accomplishments:
* **Code Refinement:** Updated `src/integrators.py` to support `t_eval`, allowing for direct comparison of asynchronous adaptive time-steps.
* **Extended Simulation:** Increased horizon to $t=60$ to track long-term divergence.
* **Analysis:** Generated `plots/butterfly_extended.png` and `plots/divergence_plot.png`.

### Technical Observations:
* **The Broadcasting Success:** Using `t_eval` fixed the dimensionality mismatch caused by the adaptive stepper's response to the perturbation.
* **Divergence Rate:** The distance $||\Delta y||$ grew from $10^{-4}$ to $\approx 2 \times 10^{-2}$ over 60 time units. While the orbit visually maintains its shape, the log-scale plot reveals a clear, oscillating upward trend.
* **Lyapunov Signature:** The linear slope on the semi-log plot is the "signature" of exponential divergence. The oscillations correspond to the orbital frequency, showing that chaos is most active during high-velocity close encounters.

**Current Status:** Chaos is quantified. The Figure-Eight is mathematically unstable, though numerically resilient over short-to-medium time scales.

## April 25, 2026
**Status:** Saturday Sprint - Symplectic Integration & Performance Benchmarking  
**Focus:** Solving numerical energy dissipation in long-term 3-body simulations.

### Part 1: Architectural Implementation (The Build)
The primary goal of today's research was to transition from general-purpose adaptive solvers to a **Symplectic Integrator**. While SciPy’s RK45 is highly precise for short-term dynamics, it lacks the geometric properties required to conserve the Hamiltonian (Total Energy) of a gravitational system over extended time horizons.

#### Key Developments:
* **Physics Refactoring:** Implemented `compute_accelerations` in `src/physics.py`. Unlike the standard state-vector derivative, this function isolates the gravitational force calculation, allowing for the staggered updates of positions and velocities required by the Verlet algorithm.
* **Engine Development:** Authored a custom **Velocity-Verlet** solver in `src/integrators.py`. This implementation uses a "leapfrog" approach, updating velocity at the half-step ($t + \Delta t/2$) before computing the final position and acceleration at $t + \Delta t$.

**The implemented Velocity-Verlet update rule:**
1. $$v\left(t + \frac{\Delta t}{2}\right) = v(t) + \frac{1}{2} a(t) \Delta t$$
2. $$r(t + \Delta t) = r(t) + v\left(t + \frac{\Delta t}{2}\right) \Delta t$$
3. $$v(t + \Delta t) = v\left(t + \frac{\Delta t}{2}\right) + \frac{1}{2} a(t + \Delta t) \Delta t$$

---

### Part 2: The Integrator Showdown (The Result)
To verify the engine's efficacy, a "torture test" was conducted over $t=100$ time units, comparing the stability of the Figure-Eight orbit under the standard RK45 vs. the new Velocity-Verlet engine.

#### Technical Observations (integrator_comparison.png):
* **Secular Drift in RK45:** The adaptive SciPy solver shows a clear, monotonic increase in relative energy error. This "energy leak" is a signature of non-symplectic integrators, where numerical dissipation slowly alters the system's total Hamiltonian over time.
* **Bounded Error in Velocity-Verlet:** Despite using a fixed time step ($\Delta t = 0.005$), the Verlet engine maintains **stochastic stability**. The energy error oscillates due to the resolution of the step, but the mean error remains constant. It does not drift, ensuring the system remains physically consistent indefinitely.

#### Quantitative Chaos (divergence_plot.png):
The Lyapunov divergence plot confirms that while the Figure-Eight is a mathematical solution, it is dynamically unstable. A $10^{-4}$ perturbation grew exponentially to $\Delta y_{final} \approx 2 \times 10^{-2}$ over 60 time units. The rate of divergence peaked during high-velocity close encounters in the central gravitational well, as evidenced by the periodic "spikes" in the phase-space distance.

### Scientific Conclusion:
The implementation of a symplectic engine is a critical milestone for the project. While the Figure-Eight is visually stable in both solvers, the Velocity-Verlet engine is the only one that truly respects the conservation laws of physics for long-duration studies. This establishes a robust framework for investigating the "point of no return" in chaotic stellar ejections.

**Current Status:** Phase 2 (Validation) and Phase 3 (Chaos) are complete. The lab is now fully equipped with a long-term stable research engine.

## May 2, 2026
**Status:** Ejection Thresholds & Mathematical Validation

**Focus:** Finding the point of no return and proving the engine on real-world Keplerian systems.

### Accomplishments:
* **Sensitivity Sweep:** Authored `scripts/run_sensitivity_sweep.py` to incrementally inject kinetic energy into the Figure-Eight orbit. 
* **Discovery:** Identified the critical velocity perturbation threshold ($\delta \approx 0.5$). Below this, the chaotic system remains gravitationally bound. Above this, the kinetic energy overcomes the binding energy, snapping the system.
* **Cinematic Rendering:** Created a momentum-balanced visualization script (`scripts/animate_collapse.py`) to capture the total system collapse and a 1-star ejection while keeping the center-of-mass anchored.
* **Solar System Validation:** To prove the Verlet integrator doesn't just work on abstract chaos, I tested it on the Sun, Earth, and Jupiter. By switching to Astronomical Units and setting $G = 4\pi^2$, the simulation perfectly rendered 12 years of stable, closed Keplerian orbits without a single drop of energy leakage.
* **Codebase Polish:** Finalized the public API in `src/__init__.py` and successfully configured the linter to respect standard physics notation (capital `G`).

### Scientific Conclusion:
The 3-Body Laboratory is complete. What started as a basic RK45 ODE solver evolved into a custom symplectic physics engine capable of quantifying chaos, visualizing total system disintegration, and modeling real-world orbital mechanics. The architectural separation of the physics, the integrators, and the experiment scripts proved to be a highly resilient software design.