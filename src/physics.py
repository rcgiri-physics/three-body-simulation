import numpy as np

def get_derivatives(t:float, state:np.ndarray, masses:np.ndarray, G:float=1.0) -> np.ndarray:
    """
    Calculates the derivatives for a 3-body system in a 2D plane.
    
    State vector structure (12 elements):
    [x1, y1, x2, y2, x3, y3, vx1, vy1, vx2, vy2, vx3, vy3]
    """
    # 1. Unpack and Reshape
    # Positions: (3 bodies, 2 coordinates)
    pos = state[:6].reshape((3, 2))
    # Velocities: (3 bodies, 2 coordinates)
    vel = state[6:].reshape((3, 2))
    
    # 2. Prepare the acceleration container
    accel = np.zeros((3, 2))
    
    # 3. Calculate Gravitational Pull
    for i in range(3):
        for j in range(3):
            if i == j:
                continue # A body doesn't pull itself
            
            # Vector from body i to body j
            r_vec = pos[j] - pos[i]
            
            # Distance (Magnitude of the vector)
            dist = np.linalg.norm(r_vec)
            
            # Newton's Law: a = G * m_j * r_vec / dist^3
            accel[i] += G * masses[j] * r_vec / (dist**3)
            
    # 4. Repack into a flat 1D array for the solver
    derivatives = np.zeros(12)
    derivatives[:6] = vel.flatten()   # dr/dt = v
    derivatives[6:] = accel.flatten() # dv/dt = a
    
    return derivatives

def calculate_energy(state, masses, G=1.0):
    """
    Calculates the total energy (Kinetic + Potential) of the 3-body system.
    """
    # 1. Reshape for easy math
    pos = state[:6].reshape((3, 2))
    vel = state[6:].reshape((3, 2))
    
    # 2. Kinetic Energy (T = sum of 1/2 * m * v^2)
    ke = 0
    for i in range(3):
        v_sq = np.dot(vel[i], vel[i])
        ke += 0.5 * masses[i] * v_sq
        
    # 3. Potential Energy (V = -sum of G*mi*mj / rij)
    pe = 0
    for i in range(3):
        for j in range(i + 1, 3): # Avoid double counting and self-interaction
            r_vec = pos[j] - pos[i]
            dist = np.linalg.norm(r_vec)
            pe -= (G * masses[i] * masses[j]) / dist
            
    return ke + pe, ke, pe

def compute_accelerations(pos, masses, G=1.0):
    pos_rs = pos.reshape((3,2))
    acc = np.zeros((3,2))

    for i in range(3):
        for j in range(3):
            if i==j: continue
            r_vec = pos_rs[j] - pos_rs[i]
            dist = np.linalg.norm(r_vec)
            acc[i] += G*masses[j] * r_vec / (dist**3)
    return acc.flatten()