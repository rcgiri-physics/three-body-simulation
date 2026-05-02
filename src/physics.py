# pylint: disable=invalid-name
"""
Core physics calculations for the N-Body gravity engine.
"""
import numpy as np


def compute_accelerations(pos, masses, G=1.0, softening=0.0001):
    """Calculates vectorized accelerations with gravitational softening."""
    # ADDED THIS LINE: Reshape flat position array to (3,2)
    pos_rs = pos.reshape((3, 2))

    # 1. Broadcasting to get all r_vecs at once. Shape: (3, 3, 2)
    diff = pos_rs[np.newaxis, :, :] - pos_rs[:, np.newaxis, :]

    # 2. Distance squared. Shape: (3, 3)
    dist_sq = np.sum(diff**2, axis=-1)

    # 3. Softened denominator. Shape: (3, 3)
    inv_dist_cubed = (dist_sq + softening**2) ** -1.5

    # 4. Remove self-interaction (diagonal)
    np.fill_diagonal(inv_dist_cubed, 0.0)

    # 5. Multiply by masses and sum along the j-axis. Shape: (3, 2)
    acc = G * np.sum(
        diff * masses[np.newaxis, :, np.newaxis] * inv_dist_cubed[:, :, np.newaxis],
        axis=1,
    )
    return acc.flatten()


def get_derivatives(
    _t: float, state: np.ndarray, masses: np.ndarray, G: float = 1.0
) -> np.ndarray:
    """
    Calculates the derivatives for a 3-body system in a 2D plane.
    """
    vel = state[6:]  # Extract velocities

    # Use the new, fast, softened acceleration function!
    accel = compute_accelerations(state[:6], masses, G, softening=0.0001)

    derivatives = np.zeros(12)
    derivatives[:6] = vel  # dr/dt = v
    derivatives[6:] = accel  # dv/dt = a

    return derivatives


def calculate_energy(state, masses, G=1.0):
    """Calculates the total energy (Kinetic + Potential)."""
    pos = state[:6].reshape((3, 2))
    vel = state[6:].reshape((3, 2))

    ke = np.sum(0.5 * masses * np.sum(vel**2, axis=1))

    pe = 0
    for i in range(3):
        for j in range(i + 1, 3):
            r_vec = pos[j] - pos[i]
            dist = np.linalg.norm(r_vec)
            pe -= (G * masses[i] * masses[j]) / dist

    return ke + pe, ke, pe


def check_ejection(state, threshold=15.0):
    """Returns True if any two bodies are separated by more than the threshold."""
    pos = state.reshape(-1, 2)[:3]
    # Calculate distances between the bodies
    d12 = np.linalg.norm(pos[0] - pos[1])
    d13 = np.linalg.norm(pos[0] - pos[2])
    d23 = np.linalg.norm(pos[1] - pos[2])

    # If any two bodies are too far apart, the system is broken
    return max(d12, d13, d23) > threshold
