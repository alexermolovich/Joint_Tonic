import numpy as np


def parse_action_tokens(tokens: np.ndarray, vocabulary: np.ndarray
                        ) -> tuple[np.ndarray, np.ndarray]:
    """Return action-bin indices and termination flags from complete token rows."""
    # Reject malformed rows before returning independent int64 arrays.
    pass
