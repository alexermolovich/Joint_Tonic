import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def nominal(m):
    out, valid = m.interpolate_joint_state([0, 1, 2], [[0, 2], [1, 4], [2, 6]], [.25, 1.5], 1)
    assert_allclose(out, [[.25, 2.5], [1.5, 5]], rtol=1e-7, atol=1e-9)
    assert_array_equal(valid, [True, True])


def dropout(m):
    out, valid = m.interpolate_joint_state([0, 2, 5], [[0], [2], [8]], [2, 3, 6], 2)
    assert_allclose(out, [[2], [np.nan], [np.nan]], equal_nan=True)
    assert_array_equal(valid, [True, False, False])


def exact_boundaries(m):
    out, valid = m.interpolate_joint_state([0, 3, 8], [[4], [7], [9]], [8, 0, 3, -1, 9, 1], .1)
    assert_allclose(out[:, 0], [9, 4, 7, np.nan, np.nan, np.nan], equal_nan=True)
    assert_array_equal(valid, [True, True, True, False, False, False])


def gap_equality_and_unsorted(m):
    out, valid = m.interpolate_joint_state([0, 1, 3], [[0], [10], [30]], [2, .5, 2, 1.5], 1)
    assert_allclose(out[:, 0], [np.nan, 5, np.nan, np.nan], equal_nan=True)
    assert_array_equal(valid, [False, True, False, False])


def empty_and_dtype(m):
    out, valid = m.interpolate_joint_state(np.array([0, 1], np.int32), np.zeros((2, 3), np.float32), [], 1)
    assert out.shape == (0, 3) and valid.shape == (0,)
    assert out.dtype == np.float64 and valid.dtype == np.bool_
    out, valid = m.interpolate_joint_state([0, 1], [[1], [2]], [.5], 1)
    assert out.dtype == np.float64 and valid.dtype == np.bool_


def malformed(m):
    good = [[0, 1], [[0], [1]], [.5], 1]
    changes = [(0, [0]), (0, [0, 0]), (0, [1, 0]), (0, [[0, 1]]),
               (1, [0, 1]), (1, np.empty((2, 0))), (1, [[0], [1], [2]]),
               (2, .5), (3, 0), (3, -1), (3, [1])]
    for index, value in changes:
        args = good.copy(); args[index] = value
        with np.testing.assert_raises(ValueError):
            m.interpolate_joint_state(*args)


def invalid_values(m):
    good = [[0, 1], [[0], [1]], [.5], 1]
    for i in range(4):
        for bad in [np.nan, np.inf, -np.inf, 1000001, 1j, "0.5", True]:
            args = good.copy()
            args[i] = ([0, bad] if i == 0 else [[0], [bad]] if i == 1 else [bad] if i == 2 else bad)
            # Mixed booleans become integer dtype; pure boolean arrays are invalid.
            if bad is True:
                args[i] = ([False, True] if i == 0 else [[False], [True]] if i == 1 else [True] if i == 2 else True)
            with np.testing.assert_raises(ValueError):
                m.interpolate_joint_state(*args)


def linear_scale_and_immutability(m):
    rng = np.random.default_rng(20261113)
    times = np.arange(1001, dtype=np.float64)
    q = np.column_stack([2 * times + 3, -times + 5, np.full_like(times, 7)])
    queries = rng.uniform(0, 1000, 20000)
    snapshots = [a.copy() for a in (times, q, queries)]
    out, valid = m.interpolate_joint_state(times, q, queries, 1)
    assert_allclose(out, np.column_stack([2 * queries + 3, -queries + 5, np.full_like(queries, 7)]), rtol=1e-7, atol=1e-9)
    assert valid.all()
    for original, snapshot in zip((times, q, queries), snapshots):
        assert_array_equal(original, snapshot)
        assert not np.shares_memory(out, original)
        assert not np.shares_memory(valid, original)


TESTS = [("Interpolate two joints", "public", nominal), ("Dropout and outside range", "public", dropout),
         ("Exact endpoints and long gaps", "hidden", exact_boundaries), ("Gap equality and query order", "hidden", gap_equality_and_unsorted),
         ("Empty outputs and dtype", "hidden", empty_and_dtype), ("Invalid shapes and ordering", "hidden", malformed),
         ("Invalid numeric values", "hidden", invalid_values), ("Linear motion at scale; no mutation", "hidden", linear_scale_and_immutability)]
