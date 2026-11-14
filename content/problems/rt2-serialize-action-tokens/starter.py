import numpy as np


def serialize_action_tokens(bins: np.ndarray, vocabulary: np.ndarray,
                            termination: np.ndarray) -> np.ndarray:
    """Return each termination flag followed by vocabulary-mapped action bins."""
    # Validate the contract and construct a fresh int64 token array.
    pass
