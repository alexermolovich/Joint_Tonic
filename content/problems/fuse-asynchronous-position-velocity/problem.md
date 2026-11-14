# Fuse Asynchronous Position and Velocity Sensors

Predict to each sensor timestamp and fuse scalar position or velocity observations in arrival order.

```python
def fuse_async_sensors(x, P, start_time, events, variances, spectral_density):
```

## Contract

Each event is [timestamp,kind,value], kind=0 position or 1 velocity. Measurement variances must be >1e-10. spectral_density q is a nonnegative scalar. Covariances must be symmetric within absolute tolerance 1e-10 and positive semidefinite (eigenvalues >=-1e-10); use their symmetrized values. Use constant velocity with continuous white acceleration: F=[[1,dt],[0,1]], Q=q*[[dt³/3,dt²/2],[dt²/2,dt]]. Fuse each scalar observation with the corresponding row of identity and Joseph covariance. Return posterior states after every event. Empty event arrays (0,3) return correctly shaped empty outputs.

**Shapes and outputs:** x(2,), P(2,2), events(N,3), variances(N,) -> means float64(N,2), covariances float64(N,2,2).

**Units:** state: position metres, velocity metres/second, time: seconds, variances: m² for position, m²/s² for velocity, spectral_density: m²/s³. **Time:** Nondecreasing event timestamps >=start_time. Simultaneous events are processed in supplied row order.

Numeric inputs are converted with np.asarray and must then have integer or floating dtype (CPU). Boolean, string, complex, and object dtypes are rejected; mixed lists follow NumPy coercion. NaN/Inf and magnitudes above 1e9 raise ValueError. Other contract violations also raise ValueError. Do not mutate inputs. Outputs are new arrays unless stated otherwise. Numerical tolerance: rtol=1e-7, atol=1e-9. Runtime: Python 3.12.3, NumPy 2.2.4; 18 s wall, 10 s CPU, 4096 MiB address space, 64 KiB output. Fixtures are original synthetic CC0-1.0 data.

## Worked examples

1. `x=[0,0], P=eye(2), start_time=0, events=[[0,0,2],[0,1,4]], variances=[1,1], spectral_density=0` → means `[[1,0],[1,2]]`, covariances `[diag([0.5,1]),diag([0.5,0.5])]`.
2. `x=[0,1], P=zeros((2,2)), start_time=0, events=[[2,0,2]], variances=[1], spectral_density=0` → means `[[2,1]]`, covariance all zeros.

Covariance numerical convention: after symmetrization, accepted eigenvalues in [-1e-10,0) are projected to zero before filtering. Eigenvalues below -1e-10 are rejected. Strictly positive observation/gating covariance still requires eigenvalues >1e-10.
