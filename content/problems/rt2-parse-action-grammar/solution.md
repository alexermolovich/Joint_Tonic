# Reference solution

Validate the supplied token rows and unique nonreserved vocabulary. Build the inverse token-to-bin mapping, decode every action field and copy the termination column independently. Any unknown token rejects the whole batch. Building the lookup and decoding take O(K+BD) expected time after O(K log K) uniqueness validation, with O(K+BD) working/output storage.

~~~python
import numpy as np


def parse_action_tokens(tokens, vocabulary):
    for value in (tokens, vocabulary):
        if not isinstance(value, np.ndarray):
            raise TypeError("Expected NumPy arrays")
        if value.dtype != np.int64:
            raise ValueError("Expected int64 arrays")
    if tokens.ndim != 2 or not 0 <= tokens.shape[0] <= 1024 or not 2 <= tokens.shape[1] <= 65:
        raise ValueError("Invalid token row shape")
    if vocabulary.ndim != 1 or not 2 <= vocabulary.size <= 4096:
        raise ValueError("Invalid vocabulary shape")
    if np.any(vocabulary < 2) or np.any(vocabulary > 1_000_000) or np.unique(vocabulary).size != vocabulary.size:
        raise ValueError("Vocabulary must contain unique nonreserved IDs")
    if np.any((tokens[:, 0] != 0) & (tokens[:, 0] != 1)):
        raise ValueError("Invalid termination flag")
    inverse = {int(token): index for index, token in enumerate(vocabulary)}
    try:
        values = [inverse[int(token)] for token in tokens[:, 1:].flat]
    except KeyError:
        raise ValueError("Unknown token in an action field") from None
    bins = np.array(values, dtype=np.int64).reshape(tokens.shape[0], tokens.shape[1] - 1)
    return bins, tokens[:, 0].copy()

~~~

This solves the declared component only; it does not reproduce a trained robot policy or a paper benchmark.
