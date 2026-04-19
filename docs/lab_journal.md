# Research Journal: Chaotic 3-Body Dynamics

## April 19, 2026

**Status:** Day 1 - The Setup

Today was mostly about getting the house in order before the real math starts. I set up a professional folder structure (`src`, `docs`, `data`, etc.) to keep things clean from the start.

### What I did

* **The Repo:** Set up a deep `.gitignore` so I don't accidentally upload giant data files later.

* **The Math:** Sat down and mapped out the "State Vector." For 3 bodies in a 2D plane, I'm going to need to track 12 variables (position and velocity for each).

* **The Logic:** Decided to use **Dimensionless Units** ($G=1$). It makes the equations much cleaner and avoids those tiny decimals that usually crash simulations.

### Key Insight

I realized that using the vector form $\mathbf{a} = G m \frac{\mathbf{r}}{r^3}$ is much easier to code than trying to calculate angles with sine and cosine. It handles the direction automatically.

### Next Step

Start writing the actual `get_derivatives` function in `src/physics.py`. I'll start with just 2 bodies to make sure they orbit correctly before I add the third one and let the chaos begin.
