# Physics of the 3-Body Problem (2D)

## 1. The State Vector

To solve the system using an ODE integrator (like RK4), we define a state vector $y$ containing 12 variables:
$$y = [x_1, y_1, x_2, y_2, x_3, y_3, v_{x1}, v_{y1}, v_{x2}, v_{y2}, v_{x3}, v_{y3}]$$

## 2. Equations of Motion

The derivative of the state vector $\frac{dy}{dt}$ is:
$$\frac{dy}{dt} = [v_{x1}, v_{y1}, v_{x2}, v_{y2}, v_{x3}, v_{y3}, a_{x1}, a_{y1}, a_{x2}, a_{y2}, a_{x3}, a_{y3}]$$

Where acceleration $\mathbf{a}_i$ for body $i$ is calculated as:
$$\mathbf{a}_i = \sum_{j \neq i} \frac{G m_j (\mathbf{r}_j - \mathbf{r}_i)}{|\mathbf{r}_j - \mathbf{r}_i|^3}$$

## 3. Numerical Stability

- **Units:** We use Dimensionless Units ($G=1$).
- **Softening Factor:** To avoid infinite forces during "close encounters," we may implement a tiny softening factor $\epsilon$ in the denominator: $(r^2 + \epsilon^2)^{1.5}$.
