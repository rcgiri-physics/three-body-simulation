"""
Generates an animation of the 3-body system collapsing and ejecting a star.
"""

import os

os.makedirs("plots", exist_ok=True)

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
# Use python -m scripts.animate_collapse to run file direcltly from root

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.integrators import run_verlet_simulation


def create_collapse_animation():
    """Module to animate collapse"""
    print("Generating system collapse data...")

    # 1. Setup Initial Conditions with the DEADLY perturbation (delta = 0.5)
    x0 = 0.97000436
    y0 = -0.24308753
    vx0 = -0.4662036850
    vy0 = -0.4323657300
    masses = np.array([1.0, 1.0, 1.0])
    delta = 0.5

    state_0 = np.array(
        [
            x0,
            y0,
            -x0,
            -y0,
            0.0,
            0.0,
            vx0 - (delta / 2),
            vy0,
            vx0 - (delta / 2),
            vy0,
            -2 * vx0 + delta,
            -2 * vy0,
        ]
    )

    # 2. Run the Engine (We only need to go to t=15 since it breaks at t=11.91)
    dt = 0.01
    t_max = 15.0
    times, history = run_verlet_simulation(state_0, masses, t_span=(0, t_max), dt=dt)

    # Extract positions for all 3 bodies over time
    # history shape is (num_steps, 12). We want (num_steps, 3 bodies, 2 coords)
    pos_data = history[:6, :].T.reshape(-1, 3, 2)

    print("Data generated. Rendering animation (this may take a minute)...")

    # 3. Setup the Plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    # We want a wide view to see the star fly away
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_title(f"Stellar Ejection (Perturbation = {delta})", color="white", pad=20)
    ax.axis("off")  # Hide axes for a cinematic look

    # Colors for the stars
    colors = ["cyan", "magenta", "yellow"]

    # Create line objects for the trails and scatter objects for the stars
    lines = [ax.plot([], [], color=colors[i], alpha=0.7, lw=1.5)[0] for i in range(3)]
    stars = [
        ax.plot([], [], marker="o", color=colors[i], markersize=8)[0] for i in range(3)
    ]

    # 4. The Animation Function
    # To make the GIF render faster and look smoother, we skip frames
    frame_step = 5
    trail_length = 100  # How many previous positions to draw

    def update(frame):
        # Calculate the actual index in our data array
        idx = frame * frame_step

        for i in range(3):
            # Get the trail history
            start_idx = max(0, idx - trail_length)
            x_trail = pos_data[start_idx:idx, i, 0]
            y_trail = pos_data[start_idx:idx, i, 1]

            # Update the trail line
            lines[i].set_data(x_trail, y_trail)

            # Update the current star position
            stars[i].set_data([pos_data[idx, i, 0]], [pos_data[idx, i, 1]])

        return lines + stars

    # 5. Render and Save
    total_frames = len(times) // frame_step
    ani = animation.FuncAnimation(
        fig, update, frames=total_frames, interval=20, blit=True
    )

    # Save as GIF using Pillow
    output_path = "plots/system_collapse.gif"
    ani.save(output_path, writer="pillow", fps=30)

    print(f"Animation successfully saved to {output_path}!")


if __name__ == "__main__":
    create_collapse_animation()
