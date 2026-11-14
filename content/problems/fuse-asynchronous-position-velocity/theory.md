# Fuse Asynchronous Position and Velocity Sensors

## Intuition

Position and velocity sensors often publish at different rates. Instead of fabricating simultaneous samples, advance the state to the next event time and update only the component that sensor actually observes.

## Mathematics and physical meaning

State $x=[p,v]^\top$ contains position in metres and velocity in metres/second. Between event times separated by $\Delta t\ge0$ seconds, use
$$F=\begin{bmatrix}1&\Delta t\\0&1\end{bmatrix},\quad Q=q\begin{bmatrix}\Delta t^3/3&\Delta t^2/2\\\Delta t^2/2&\Delta t\end{bmatrix}.$$
Here $q$ is continuous acceleration-noise spectral density in m²/s³, not a per-step acceleration variance. Predict $x^-=Fx$, $P^-=FPF^\top+Q$. For event kind $j\in\{0,1\}$, measurement $z$, variance $r>0$, and unit basis vector $e_j$, use
$$s=P^-_{jj}+r,\quad K=P^-e_j/s,\quad x^+=x^-+K(z-x^-_j).$$
With $A=I-Ke_j^\top$, Joseph covariance is $P^+=AP^-A^\top+rKK^\top$. Each output records this posterior before processing the next event.

## Visual trace

| Event | Predict interval | Observation row | State stored |
|---|---|---|---|
| Position at 0 s | 0 s | [1,0] | posterior at 0 s |
| Velocity at 1 s | 1 s | [0,1] | posterior at 1 s |
| Position at 1 s | 0 s | [1,0] | second posterior at 1 s |

This static table is also the text alternative; no animation is required.

## Worked examples

1. `x=[0,0], P=eye(2), start_time=0, events=[[0,0,2],[0,1,4]], variances=[1,1], spectral_density=0` → means `[[1,0],[1,2]]`, covariances `[diag([0.5,1]),diag([0.5,0.5])]`.
2. `x=[0,1], P=zeros((2,2)), start_time=0, events=[[2,0,2]], variances=[1], spectral_density=0` → means `[[2,1]]`, covariance all zeros.

## Why this matters on a robot

Updating at arrival time instead of capture time creates motion-dependent bias. This contract assumes timestamps already share one clock and rejects out-of-order events; delayed-state smoothing and frame conversion are outside this task.

## Sources and prerequisites

- [Primary reference 1](https://www.cs.cmu.edu/~motionplanning/papers/sbp_papers/kalman/welch_intro_kalman.pdf)

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
