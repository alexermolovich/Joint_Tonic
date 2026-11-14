"""Sample Mass, Friction, Delay, and Gain Distributions."""
import numpy as np


def sample_dynamics(unit_draws: np.ndarray,
                    bounds: dict[str, tuple[float, float]],
                    dt_s: float) -> dict[str, np.ndarray]:
    """Transform supplied unit draws; do not generate new randomness."""
    raise NotImplementedError("Implement sample_dynamics")
