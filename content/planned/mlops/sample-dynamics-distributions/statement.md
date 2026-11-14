# Sample Mass, Friction, Delay, and Gain Distributions

**Draft 0.1.0 — not runnable yet.**

Turn recorded unit-interval draws into a small physical configuration for each simulated episode. Keep the transform deterministic so an unexpected rollout can be replayed.

## Function contract

~~~python
import numpy as np

def sample_dynamics(unit_draws: np.ndarray,
                    bounds: dict[str, tuple[float, float]],
                    dt_s: float) -> dict[str, np.ndarray]:
    ...
~~~

unit_draws is a CPU NumPy float64 array of shape (B,4), 0 ≤ B ≤ 10,000. Every entry is finite in [0,1), excluding 1. Columns are **mass, friction, delay, gain**, in that order. A caller may generate independent uniform draws using a recorded seed; this function consumes the supplied values and must not call any random generator.

bounds is a dict with exactly four keys:

| Key | Bounds and meaning |
|---|---|
| mass_kg | positive object-mass range [a,b], in kilograms |
| friction | positive dimensionless Coulomb-friction range [a,b] |
| delay_ticks | inclusive integer [lo,hi] of control delay |
| gain_scale | positive dimensionless multiplier of a fixed baseline controller gain |

Each value is a two-item tuple. Mass/friction/gain endpoints are finite built-in int/float values excluding bool, satisfying 1e-9 ≤ a ≤ b ≤ 1e6. Delay endpoints must be built-in ints excluding bool, with 0 ≤ lo ≤ hi ≤ 10,000. dt_s is a finite built-in int/float excluding bool, with 1e-6 ≤ dt_s ≤ 1 second per control tick.

For a positive parameter and its unit draw u, return exp(log(a) + u*(log(b)-log(a))). For delay return lo + floor(u*(hi-lo+1)). Equal endpoints produce a fixed parameter.

Return exactly five new arrays, all shape (B,): mass_kg, friction, gain_scale, delay_s with dtype float64, and delay_ticks with dtype int64. delay_s equals delay_ticks multiplied by dt_s. Numeric outputs use rtol=1e-12 and atol=1e-12 in their declared units; integer delays are exact. Preserve all inputs.

Each row specifies one episode reset. Parameters remain fixed through that episode; this function does not execute physics, resample at each timestep, change reference frames, or define an actuator buffer. Scalars have no spatial axes. Using the sampled delay later means a fixed number of control ticks, not physics substeps.

## Errors and empty inputs

Raise ValueError for wrong types/dtypes/shapes, missing or extra bounds, invalid values/ranges, or exceeded limits. Reject zero friction because the log transform requires positive support. Error messages are not graded. Shape (0,4) returns five correctly typed empty arrays after validating bounds and dt_s. Torch tensors and float32 draws are rejected.

## Worked example 1 — lower endpoint and log midpoint

~~~python
unit_draws = np.array([[0., 0., 0., 0.],
                      [0.5, 0.5, 0.5, 0.5]], dtype=np.float64)
bounds = {"mass_kg": (1., 9.), "friction": (0.25, 1.),
          "delay_ticks": (0, 3), "gain_scale": (0.5, 2.)}
dt_s = 0.01
# Values (each is an array with the dtype specified above):
# mass_kg: [1., 3.]       friction: [0.25, 0.5]
# delay_ticks: [0, 2]    gain_scale: [0.5, 1.]
# delay_s: [0., 0.02]
~~~

The mass midpoint is the geometric mean 3 kg, not the arithmetic midpoint 5 kg. Half the delay unit interval maps to tick 2 because there are four possible integers.

## Worked example 2 — a fixed configuration

~~~python
unit_draws = np.array([[0.75, 0.25, 0.9, 0.1]], dtype=np.float64)
bounds = {"mass_kg": (2., 2.), "friction": (0.5, 0.5),
          "delay_ticks": (1, 1), "gain_scale": (1., 1.)}
dt_s = 0.02
# mass_kg: [2.]          friction: [0.5]
# delay_ticks: [1]       gain_scale: [1.]
# delay_s: [0.02]
~~~

Collapsed ranges ignore the supplied draw's position but still require every draw to be valid.
