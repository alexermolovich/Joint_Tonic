import numpy as np


def receding_horizon_window(
    trajectory: np.ndarray, valid: np.ndarray, offset: int, execute_steps: int
) -> np.ndarray:
    """Return a copied execution buffer only when every selected tick is valid."""
    pass
