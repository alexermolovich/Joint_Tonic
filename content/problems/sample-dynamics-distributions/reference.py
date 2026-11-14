import math
import numpy as np


def sample_dynamics(unit_draws: np.ndarray,
                    bounds: dict[str, tuple[float, float]],
                    dt_s: float) -> dict[str, np.ndarray]:
    if not isinstance(unit_draws, np.ndarray) or unit_draws.dtype != np.float64:
        raise ValueError("Expected float64 NumPy draws")
    if unit_draws.ndim != 2 or unit_draws.shape[1] != 4 or unit_draws.shape[0] > 10000:
        raise ValueError("Expected at most 10000 four-column rows")
    if not np.isfinite(unit_draws).all() or np.any(unit_draws < 0) or np.any(unit_draws >= 1):
        raise ValueError("Unit draws must be finite in [0,1)")
    names = {"mass_kg", "friction", "delay_ticks", "gain_scale"}
    if not isinstance(bounds, dict) or set(bounds) != names:
        raise ValueError("Expected exactly four physical bounds")
    for name, interval in bounds.items():
        if not isinstance(interval, tuple) or len(interval) != 2:
            raise ValueError("Each bound must be a two-item tuple")
        lower, upper = interval
        if name == "delay_ticks":
            if type(lower) is not int or type(upper) is not int or not 0 <= lower <= upper <= 10000:
                raise ValueError("Invalid delay-tick bounds")
        elif (type(lower) not in (int, float) or type(upper) not in (int, float)
              or not 1e-9 <= lower <= upper <= 1e6):
            raise ValueError("Invalid positive parameter bounds")
    if type(dt_s) not in (int, float) or not 1e-6 <= dt_s <= 1 or not math.isfinite(dt_s):
        raise ValueError("Invalid control timestep")
    output = {}
    for name, column in (("mass_kg", 0), ("friction", 1), ("gain_scale", 3)):
        lower, upper = bounds[name]
        output[name] = np.exp(np.log(lower) + unit_draws[:, column] * (np.log(upper) - np.log(lower)))
    lower, upper = bounds["delay_ticks"]
    output["delay_ticks"] = lower + np.floor(unit_draws[:, 2] * (upper - lower + 1)).astype(np.int64)
    output["delay_s"] = output["delay_ticks"] * float(dt_s)
    return output
