"""Original deterministic action fixtures; CC0-1.0."""
import copy
import numpy as np


def _raises(kind, fn):
    try:
        fn()
    except kind:
        return
    raise AssertionError(f"expected {kind.__name__}")


def bounds(m):
    tokens, decoded = m.action_codec([[-1.], [0.], [1.]], [-1.], [1.], bins=4)
    np.testing.assert_array_equal(tokens, [[0], [2], [3]])
    np.testing.assert_allclose(decoded, [[-0.75], [0.25], [0.75]])


def offset_and_clipping(m):
    tokens, decoded = m.action_codec([[-5., 9.]], [0., 0.], [2., 8.], 2, 100)
    np.testing.assert_array_equal(tokens, [[100, 101]])
    np.testing.assert_allclose(decoded, [[0.5, 6.]])


def single_action(m):
    tokens, decoded = m.action_codec([0.25, 0.75], [0., 0.], [1., 1.], 2)
    assert tokens.shape == decoded.shape == (2,)
    np.testing.assert_array_equal(tokens, [0, 1])
    np.testing.assert_allclose(decoded, [0.25, 0.75])


def dimensions_and_dtype(m):
    a = np.array([[[0., 15.], [2., 20.]], [[1., 10.], [0.5, 19.]]], dtype=np.float32)
    tokens, decoded = m.action_codec(a, [0, 10], [2, 20], 4)
    assert tokens.dtype == np.int64 and decoded.dtype == np.float64
    np.testing.assert_array_equal(tokens, [[[0, 2], [3, 3]], [[2, 0], [1, 3]]])
    np.testing.assert_allclose(decoded, [[[0.25, 16.25], [1.75, 18.75]], [[1.25, 11.25], [0.75, 18.75]]])


def empty_batch(m):
    tokens, decoded = m.action_codec(np.empty((2, 0, 3)), [-1]*3, [1]*3)
    assert tokens.shape == decoded.shape == (2, 0, 3)


def reconstruction_error(m):
    a = np.random.default_rng(7).uniform(-2, 3, (100, 4))
    tokens, decoded = m.action_codec(a, [-2]*4, [3]*4, 32, 17)
    assert tokens.min() >= 17 and tokens.max() <= 48
    assert np.max(np.abs(a-decoded)) <= 5 / 64 + 1e-12


def immutable(m):
    a = np.array([[0., 4.]])
    low, high = np.array([-1., 0.]), np.array([1., 2.])
    old = [x.copy() for x in (a, low, high)]
    m.action_codec(a, low, high, 8)
    for now, before in zip((a, low, high), old):
        np.testing.assert_array_equal(now, before)


def invalid_settings(m):
    for b in (True, 2.5, "4"):
        _raises(TypeError, lambda: m.action_codec([[0]], [-1], [1], b))
    _raises(TypeError, lambda: m.action_codec([[0]], [-1], [1], 4, False))
    for b, offset in ((1, 0), (4, -1), (4, 2**63-1)):
        _raises(ValueError, lambda: m.action_codec([[0]], [-1], [1], b, offset))


def invalid_arrays(m):
    for a, lo, hi in ((0, [-1], [1]), ([[0, 1]], [-1], [1]), ([[0]], [1], [1]),
                      ([[float("inf")]], [-1], [1]), ([[0]], [0], [float("nan")])):
        _raises(ValueError, lambda: m.action_codec(a, lo, hi))


TESTS = [
    ("Exact endpoints and center boundary", "public", bounds),
    ("Clipping and token offset", "public", offset_and_clipping),
    ("One unbatched action", "public", single_action),
    ("Per-dimension batched codec", "hidden", dimensions_and_dtype),
    ("Empty leading batch dimension", "hidden", empty_batch),
    ("Maximum reconstruction error", "hidden", reconstruction_error),
    ("Input immutability", "hidden", immutable),
    ("Token-range validation", "hidden", invalid_settings),
    ("Array and bound validation", "hidden", invalid_arrays),
]
