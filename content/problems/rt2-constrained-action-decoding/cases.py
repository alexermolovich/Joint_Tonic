"""Original synthetic bounded decoder fixtures, CC0-1.0."""
import math
import numpy as np


def checked(m, logits, vocabulary, positions, channels, ids, expected):
    inputs = (logits, vocabulary, positions)
    before = [x.copy() for x in inputs]
    result = m.constrained_action_step(*inputs, channels)
    assert type(result) is tuple and len(result) == 2
    tokens, probabilities = result
    assert isinstance(tokens, np.ndarray) and tokens.dtype == np.int64 and tokens.shape == (logits.shape[0],)
    assert isinstance(probabilities, np.ndarray) and probabilities.dtype == np.float64 and probabilities.shape == logits.shape
    np.testing.assert_array_equal(tokens, ids)
    np.testing.assert_allclose(probabilities, expected, rtol=1e-6, atol=1e-7)
    for row, position in enumerate(positions):
        allowed = [0, 1] if position == 0 else vocabulary.tolist()
        blocked = [i for i in range(logits.shape[1]) if i not in allowed]
        assert np.all(probabilities[row, blocked] == 0)
        np.testing.assert_allclose(probabilities[row].sum(), 1., rtol=1e-12, atol=1e-12)
    for output in result:
        for original in inputs:
            assert not np.shares_memory(output, original)
    assert not np.shares_memory(tokens, probabilities)
    for original, snapshot in zip(inputs, before):
        np.testing.assert_array_equal(original, snapshot)
    return result


def mixed_rows(m):
    checked(m, np.array([[0., math.log(3), 50., 50., 50.], [99., 99., 0., 99., math.log(3)]]),
            np.array([4, 2], dtype=np.int64), np.array([0, 1], dtype=np.int64), 2,
            [1, 4], [[.25, .75, 0, 0, 0], [0, 0, .25, 0, .75]])


def numeric_tie(m):
    checked(m, np.zeros((1, 5)), np.array([4, 2], dtype=np.int64), np.array([2], dtype=np.int64), 2,
            [2], [[0, 0, .5, 0, .5]])


def empty_batch(m):
    checked(m, np.empty((0, 4)), np.array([3, 2], dtype=np.int64), np.empty(0, dtype=np.int64), 1,
            np.empty(0, dtype=np.int64), np.empty((0, 4)))


def oracle_noncontiguous(m):
    rng = np.random.default_rng(20261113)
    logits = rng.uniform(-100., 100., (12, 42))[:, ::2]
    vocabulary = np.array([17, 15, 11, 9, 6, 4, 2, 19], dtype=np.int64)[::-2]
    positions = np.tile(np.array([0, 1, 2, 3, 4, 5], dtype=np.int64), 4)[::2]
    expected = np.zeros_like(logits)
    ids = []
    for row, pos in enumerate(positions):
        allowed = [0, 1] if pos == 0 else vocabulary.tolist()
        # Independent scalar oracle: bounded input permits unshifted exponentials.
        denominator = math.fsum(math.exp(float(logits[row, col])) for col in allowed)
        for col in allowed:
            expected[row, col] = math.exp(float(logits[row, col])) / denominator
        ids.append(min(allowed, key=lambda col: (-float(logits[row, col]), col)))
    checked(m, logits, vocabulary, positions, 5, ids, expected)


def extremes_and_flags(m):
    checked(m, np.array([[-100., -100., 100., 100.], [100., 100., -100., -100.]]),
            np.array([3, 2], dtype=np.int64), np.array([0, 64], dtype=np.int64), 64,
            [0, 2], [[.5, .5, 0, 0], [0, 0, .5, .5]])


def rejects(m):
    args = [np.zeros((1, 5)), np.array([4, 2], dtype=np.int64), np.array([1], dtype=np.int64), 2]
    def reject(index, value, error=ValueError):
        bad = args.copy(); bad[index] = value
        with np.testing.assert_raises(error):
            m.constrained_action_step(*bad)
    for index in range(3):
        reject(index, args[index].tolist(), TypeError)
    for bad in [np.zeros((1, 5), dtype=np.float32), np.zeros(5), np.zeros((1, 3)), np.zeros((257, 5)),
                np.empty((0, 65537)), np.zeros((256, 4096)), np.full((1, 5), np.nan),
                np.full((1, 5), np.inf), np.full((1, 5), 101.), np.full((1, 5), -101.)]:
        reject(0, bad)
    for bad in [np.array([2, 4], dtype=np.int32), np.array([2., 4.]), np.array([[2, 4]], dtype=np.int64),
                np.array([], dtype=np.int64), np.array([2], dtype=np.int64), np.array([2, 2], dtype=np.int64),
                np.array([1, 2], dtype=np.int64), np.array([-1, 2], dtype=np.int64), np.array([2, 5], dtype=np.int64),
                np.array([2, 3, 4, 2], dtype=np.int64)]:
        reject(1, bad)
    for bad in [np.array([1], dtype=np.int32), np.array([1.]), np.array([[1]], dtype=np.int64),
                np.array([], dtype=np.int64), np.array([-1], dtype=np.int64), np.array([3], dtype=np.int64)]:
        reject(2, bad)
    for bad in [True, False, 0, 65, 1., np.int64(1), '1', None, 10**1000]:
        reject(3, bad)
    # Empty batches still require valid vocabularies and channel counts.
    with np.testing.assert_raises(ValueError):
        m.constrained_action_step(np.empty((0, 4)), np.array([2, 2], dtype=np.int64), np.empty(0, dtype=np.int64), 1)
    with np.testing.assert_raises(ValueError):
        m.constrained_action_step(np.zeros((1, 5000)), np.arange(2, 4099, dtype=np.int64), np.zeros(1, dtype=np.int64), 1)


def mixed_invalid_row(m):
    with np.testing.assert_raises(ValueError):
        m.constrained_action_step(np.zeros((3, 4)), np.array([2, 3], dtype=np.int64), np.array([0, 1, 3], dtype=np.int64), 2)
    with np.testing.assert_raises(ValueError):
        m.constrained_action_step(np.array([[0., 0., 0., 0.], [0., np.nan, 0., 0.]]),
                                  np.array([2, 3], dtype=np.int64), np.array([0, 1], dtype=np.int64), 1)


def large_vocabulary(m):
    # Largest declared vocabulary width, and a separate batch near the entry budget.
    for batch, width, count in [(1, 65536, 4096), (256, 3906, 3904)]:
        vocabulary = np.arange(width - 1, width - count - 1, -1, dtype=np.int64)
        positions = np.ones(batch, dtype=np.int64)
        logits = np.full((batch, width), 100.)
        logits[:, vocabulary] = -100.
        tokens, probabilities = m.constrained_action_step(logits, vocabulary, positions, 1)
        assert tokens.dtype == np.int64 and probabilities.dtype == np.float64
        np.testing.assert_array_equal(tokens, np.full(batch, vocabulary.min(), dtype=np.int64))
        expected = np.zeros((batch, width)); expected[:, vocabulary] = 1./count
        np.testing.assert_allclose(probabilities, expected, rtol=1e-6, atol=1e-7)
        assert np.all(probabilities[:, :width-count] == 0)


TESTS = [
    ("Flag and action fields normalize independently", "public", mixed_rows),
    ("Ties follow numeric token identity", "public", numeric_tie),
    ("Empty batch preserves output shapes", "public", empty_batch),
    ("Scalar probability oracle and noncontiguous views", "hidden", oracle_noncontiguous),
    ("Extreme valid logits and flag ties", "hidden", extremes_and_flags),
    ("Typed shape bounds and vocabulary validation", "hidden", rejects),
    ("Invalid rows reject the entire batch", "hidden", mixed_invalid_row),
    ("Vocabulary and batch scale", "hidden", large_vocabulary),
]
