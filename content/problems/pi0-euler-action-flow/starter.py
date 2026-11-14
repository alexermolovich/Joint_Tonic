from collections.abc import Callable
import numpy as np


def euler_action_flow(initial: np.ndarray, times: np.ndarray,
                      velocity: Callable[[np.ndarray, float], np.ndarray]
                      ) -> tuple[np.ndarray, np.ndarray]:
    """Integrate supplied action velocity with left-endpoint explicit Euler steps."""
    # Return independent final actions and a trace including the initial state.
    pass
