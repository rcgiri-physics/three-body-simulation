"""physverify spec for the planar three-body code in src/.

    physverify run tests/verify_three_body.py

The reference equations below are written from Newtonian gravity (G = 1),
with the softening length eps = 1e-4 that docs/theory.md describes:

    dr_i/dt = v_i
    dv_i/dt = sum_{j != i} m_j (r_j - r_i) / (|r_j - r_i|^2 + eps^2)^(3/2)
    E = sum_i m_i |v_i|^2 / 2 - sum_{i<j} m_i m_j / sqrt(|r_j - r_i|^2 + eps^2)

State layout used by the code: [x1, y1, x2, y2, x3, y3, vx1, vy1, ..., vy3].

What is checked:
- get_derivatives agrees with the reference right-hand side.
- verlet_step converges at second order against an independent RK4 solution,
  and its energy drift shrinks at second order.
- verlet_step keeps total momentum and angular momentum to round-off
  (pairwise central forces), and is time-reversible.
- run_verlet_simulation ends exactly at t_end.
- calculate_energy is the energy written above.
- The README energy claim: run_simulation (SciPy RK45, rtol 1e-9) on the
  setup of scripts/energy_analysis.py keeps |dE/E0| below 1e-8 up to t = 20.

Not checked: velocity Verlet has no source-term hook, so there is no
manufactured-solution check of it; the reference and invariant checks cover it.
"""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import calculate_energy, get_derivatives, run_simulation, run_verlet_simulation, verlet_step  # noqa: E402
from physverify import Check, Result, check_exact, invariant_study, reference_study, zero_source  # noqa: E402
from physverify.studies import time_grid_check  # noqa: E402

EPS = 1e-4
MASSES = np.array([1.0, 1.0, 1.0])

# A smooth, bounded test orbit: the figure-eight initial condition.
X1 = np.array([0.97000436, -0.24308753])
V3 = np.array([-0.93240737, -0.86473146])
Y0 = np.concatenate([X1, -X1, [0.0, 0.0], -V3 / 2, -V3 / 2, V3])
T_END = 1.0
NS = (200, 400, 800, 1600)


def reference_rhs(t, y, masses=MASSES):
    r = y[:6].reshape(3, 2)
    a = np.zeros((3, 2))
    for i in range(3):
        for j in range(3):
            if i != j:
                d = r[j] - r[i]
                a[i] += masses[j] * d / (d @ d + EPS**2) ** 1.5
    return np.concatenate([y[6:], a.ravel()])


def energy(y, masses=MASSES):
    r = y[:6].reshape(3, 2)
    v = y[6:].reshape(3, 2)
    e = 0.5 * sum(masses[i] * (v[i] @ v[i]) for i in range(3))
    for i in range(3):
        for j in range(i + 1, 3):
            d = r[j] - r[i]
            e -= masses[i] * masses[j] / math.sqrt(d @ d + EPS**2)
    return e


def momentum(y):
    return (MASSES[:, None] * y[6:].reshape(3, 2)).sum(axis=0)


def angular_momentum(y):
    r = y[:6].reshape(3, 2)
    v = y[6:].reshape(3, 2)
    return float(np.sum(MASSES * (r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0])))


def verlet(source, y0, t_end, n):
    if source is not zero_source:
        raise ValueError("verlet_step has no source-term hook")
    y = np.array(y0, dtype=float)
    for _ in range(n):
        y = verlet_step(y, MASSES, t_end / n)
    return y


def rhs_agrees():
    rng = np.random.default_rng(1)
    worst = 0.0
    for _ in range(50):
        y = np.concatenate([rng.uniform(-2, 2, 6), rng.uniform(-1, 1, 6)])
        ref = reference_rhs(0.0, y)
        worst = max(worst, float(np.max(np.abs(get_derivatives(0.0, y, MASSES) - ref)) / np.max(np.abs(ref))))
    if worst <= 1e-12:
        return Result("EXACT", f"agrees at 50 random states (largest relative difference {worst:.1e})")
    return Result("FAIL", f"differs from Newtonian gravity by up to {worst:.2g} (relative)")


def energy_function_agrees():
    rng = np.random.default_rng(2)
    worst = 0.0
    for _ in range(50):
        y = np.concatenate([rng.uniform(-2, 2, 6), rng.uniform(-1, 1, 6)])
        worst = max(worst, abs(float(calculate_energy(y, MASSES)[0]) - energy(y)) / abs(energy(y)))
    if worst <= 1e-12:
        return Result("EXACT", f"agrees at 50 random states (largest relative difference {worst:.1e})")
    return Result("FAIL", f"differs from the softened energy by up to {worst:.2g} (relative)")


def conserved_exactly(quantity):
    def run():
        q0 = np.atleast_1d(quantity(Y0))
        hs, errs = [], []
        for n in NS:
            hs.append(T_END / n)
            errs.append(float(np.max(np.abs(np.atleast_1d(quantity(verlet(zero_source, Y0, T_END, n))) - q0))))
        return check_exact(hs, errs)

    return run


def time_reversal():
    hs, errs = [], []
    for n in NS:
        y = verlet(zero_source, Y0, T_END, n)
        y = np.concatenate([y[:6], -y[6:]])
        y = verlet(zero_source, y, T_END, n)
        y = np.concatenate([y[:6], -y[6:]])
        hs.append(T_END / n)
        errs.append(float(np.max(np.abs(y - Y0))))
    return check_exact(hs, errs, floor=1e-11)


def readme_energy_claim():
    # Initial condition as written in scripts/energy_analysis.py.
    v3 = np.array([-0.93240737, -0.86473146])
    y0 = np.concatenate([[-0.97, 0.24], [0.97, -0.24], [0.0, 0.0], -0.5 * v3, -0.5 * v3, v3])
    sol = run_simulation(get_derivatives, (0.0, 20.0), y0, MASSES)
    e0 = energy(y0)
    worst = max(abs(energy(sol.y[:, k]) - e0) / abs(e0) for k in range(sol.y.shape[1]))
    if worst < 1e-8:
        return Result("PASS", f"largest |dE/E0| = {worst:.1e} over t in [0, 20] ({sol.y.shape[1]} RK45 steps)")
    return Result("FAIL", f"largest |dE/E0| = {worst:.2g} over t in [0, 20], above 1e-8")


def checks():
    return [
        Check("reference", "get_derivatives is softened Newtonian gravity", rhs_agrees),
        Check("reference", "verlet_step (order 2)", lambda: reference_study(verlet, reference_rhs, Y0, T_END, NS, 2.0)),
        Check("invariant", "verlet_step energy drift (order 2)", lambda: invariant_study(verlet, energy, Y0, T_END, NS, 2.0)),
        Check("invariant", "verlet_step total momentum", conserved_exactly(momentum)),
        Check("invariant", "verlet_step angular momentum", conserved_exactly(angular_momentum)),
        Check("patch", "verlet_step time reversal", time_reversal),
        Check(
            "limit",
            "run_verlet_simulation ends at t_end",
            lambda: time_grid_check(lambda n: run_verlet_simulation(Y0, MASSES, (0.0, T_END), T_END / n)[0], 0.0, T_END, (4, 8, 10, 16)),
        ),
        Check("invariant", "calculate_energy is the softened energy", energy_function_agrees),
        Check("invariant", "run_simulation (RK45) energy error, README claim", readme_energy_claim),
    ]
