![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=flat&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=flat&logo=numpy&logoColor=white)
![SciPy](https://img.shields.io/badge/scipy-%238CAAE6.svg?style=flat&logo=scipy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=flat&logo=Matplotlib&logoColor=black)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-In--Progress-orange)

# Chaotic 3-Body Dynamics: Orbital Stability

A high-precision computational study of gravitational interactions between three point-masses, exploring the boundary between periodic stability and chaotic divergence.

![The Figure-Eight 3-Body Orbit](plots/figure_eight.png)
*Figure 1: Successful verification of the Chenciner-Montgomery periodic solution. This result confirms the accuracy of the force calculation logic and the stability of the numerical integrator.*

## Research Achievements
* **Verified Periodic Stability:** Successfully reproduced the "Figure-Eight" orbit, a zero-angular-momentum solution where all three bodies follow the same spatial locus.
* **Precision Engineering:** Transitioned from basic integration to high-precision adaptive time-stepping via SciPy’s `solve_ivp` (RK45).
* **Modular Architecture:** Developed a decoupled system where the vectorized gravitational engine in `src/physics.py` is independent of the numerical integration logic.
* **Optimized Computation:** Implemented a vectorized $1/r^3$ force calculation using NumPy reshaping to bridge the gap between 2D physical coordinates and 1D state-space vectors.

## Research Objectives
1.  **State-Space Modeling:** Characterize 3-body trajectories using a 12-variable vectorized state-space.
2.  **Integrator Benchmarking:** Compare the long-term energy conservation of standard Runge-Kutta 4 (RK4) against symplectic methods.
3.  **Chaos Analysis:** Visualize and quantify the transition from stable periodic orbits to total system collapse and stellar ejection.

## Methodology & Architecture
* **Physics Engine:** Newtonian Gravity in a 2D plane using dimensionless units ($G=1$) for cleaner equations and improved numerical stability.
* **Numerical Solver:** Utilization of adaptive Runge-Kutta 4(5) with strict tolerances ($rtol=10^{-9}$, $atol=10^{-12}$) to maintain periodicity in chaotic regimes.
* **Singularity Management:** Theoretical framework established for gravitational softening $\epsilon$ to prevent infinite forces during close-stellar encounters. 
*Note on Implementation: For the present Phase (Verification via Figure-Eight), $\epsilon$ is kept at $0$ to ensure a purely Newtonian test of periodic stability. Softening will be activated in Phase 3 to manage close-encounter singularities during chaotic regimes.*
* **Validation:** Real-time monitoring of the Hamiltonian (Total Energy) to ensure physical consistency across long timescales.

## Getting Started
### Prerequisites
* Python 3.10+
* NumPy, SciPy, Matplotlib

### Installation & Execution
```bash
# Clone the repository
git clone [https://github.com/rcgiri-physics/three-body-simulation.git](https://github.com/rcgiri-physics/three-body-simulation.git)

# Install dependencies
pip install -r requirements.txt

# Run the verified Figure-Eight simulation
python -m scripts.run_simulation
```
