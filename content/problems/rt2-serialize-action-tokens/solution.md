# Reference solution

Validate the bounded integer grammar and injective vocabulary, then gather one vocabulary entry per supplied action bin. Copy the termination flag into the first column without changing action channel order. Vocabulary validation is O(K log K) using uniqueness sorting, and mapping/output storage are O(BD). The mapping is supplied explicitly rather than inferred as an offset.

~~~python
import numpy as np


def serialize_action_tokens(bins, vocabulary, termination):
    for value in (bins, vocabulary, termination):
        if not isinstance(value, np.ndarray):
            raise TypeError("Expected NumPy arrays")
        if value.dtype != np.int64:
            raise ValueError("Expected int64 arrays")
    if bins.ndim != 2 or not 0 <= bins.shape[0] <= 1024 or not 1 <= bins.shape[1] <= 64:
        raise ValueError("Invalid action shape")
    if vocabulary.ndim != 1 or not 2 <= vocabulary.size <= 4096:
        raise ValueError("Invalid vocabulary shape")
    if np.any(vocabulary < 2) or np.any(vocabulary > 1_000_000) or np.unique(vocabulary).size != vocabulary.size:
        raise ValueError("Vocabulary must contain unique nonreserved IDs")
    if termination.shape != (bins.shape[0],) or np.any((termination != 0) & (termination != 1)):
        raise ValueError("Invalid termination flags")
    if np.any(bins < 0) or np.any(bins >= vocabulary.size):
        raise ValueError("Invalid action bin")
    tokens = np.empty((bins.shape[0], bins.shape[1] + 1), dtype=np.int64)
    tokens[:, 0] = termination
    tokens[:, 1:] = vocabulary[bins]
    return tokens

~~~

This solves the declared component only; it does not reproduce a trained robot policy or a paper benchmark.
