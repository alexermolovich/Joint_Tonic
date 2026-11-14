import numpy as np


def constrained_action_step(logits, vocabulary, positions, channels):
    if not all(isinstance(x, np.ndarray) for x in (logits, vocabulary, positions)):
        raise TypeError("logits, vocabulary and positions must be arrays")
    if logits.dtype != np.float64 or logits.ndim != 2:
        raise ValueError("float64 logits (B,V) required")
    batch, width = logits.shape
    if batch > 256 or not 4 <= width <= 65536 or logits.size > 1_000_000:
        raise ValueError("logit shape budget")
    if not np.isfinite(logits).all() or (np.abs(logits) > 100).any():
        raise ValueError("finite bounded logits required")
    if vocabulary.dtype != np.int64 or vocabulary.ndim != 1:
        raise ValueError("int64 vocabulary (K,) required")
    if not 2 <= vocabulary.size <= min(4096, width-2):
        raise ValueError("vocabulary size")
    if (vocabulary < 2).any() or (vocabulary >= width).any():
        raise ValueError("action IDs must be in [2,V)")
    if np.unique(vocabulary).size != vocabulary.size:
        raise ValueError("unique action IDs required")
    if type(channels) is not int or not 1 <= channels <= 64:
        raise ValueError("bounded built-in channel count required")
    if positions.dtype != np.int64 or positions.shape != (batch,):
        raise ValueError("int64 positions (B,) required")
    if (positions < 0).any() or (positions > channels).any():
        raise ValueError("position outside fixed-width grammar")
    tokens = np.empty(batch, dtype=np.int64)
    probabilities = np.zeros_like(logits)
    action_ids = np.sort(vocabulary)
    flag_ids = np.array([0, 1], dtype=np.int64)
    for row in range(batch):
        allowed = flag_ids if positions[row] == 0 else action_ids
        scores = logits[row, allowed]
        winner = np.argmax(scores)
        weights = np.exp(scores - scores[winner])
        probabilities[row, allowed] = weights / weights.sum()
        tokens[row] = allowed[winner]
    return tokens, probabilities
