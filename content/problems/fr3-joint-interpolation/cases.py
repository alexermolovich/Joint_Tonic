import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

LOWER = np.array([-2.9007, -1.8361, -2.9007, -3.0770, -2.8763, 0.4398, -3.0508])
UPPER = np.array([2.9007, 1.8361, 2.9007, -0.1169, 2.8763, 4.6216, 3.0508])
START = np.array([0., 0., 0., -1., 0., 1., 0.])
GOAL = np.array([.4, .2, -.2, -1.4, .6, 1.4, -.4])


def result(m, a, b, n):
    value = m.interpolate_fr3_joints(a, b, n)
    assert isinstance(value, np.ndarray), "Return a NumPy array"
    assert value.dtype == np.float64, "Return float64"
    assert value.shape == (int(n), 7), "Return one seven-joint row per sample"
    return value


def midpoint(m):
    out = result(m, START.tolist(), GOAL.tolist(), 3)
    expected = [START, [.2, .1, -.1, -1.2, .3, 1.2, -.2], GOAL]
    assert_allclose(out, expected, rtol=1e-7, atol=1e-9)


def stationary(m):
    assert_allclose(result(m, START, START, 4), np.tile(START, (4, 1)), rtol=1e-7, atol=1e-9)


def two_endpoints(m):
    assert_allclose(result(m, START, GOAL, 2), [START, GOAL], rtol=1e-7, atol=1e-9)


def boundaries_and_no_wrap(m):
    out = result(m, LOWER, UPPER, 101)
    expected = np.stack([LOWER + float(k)/100 * (UPPER-LOWER) for k in range(101)])
    assert_allclose(out, expected, rtol=1e-7, atol=1e-9)
    assert_allclose(out[[0, -1]], [LOWER, UPPER], rtol=1e-7, atol=1e-9)
    assert np.all(out >= LOWER-1e-12) and np.all(out <= UPPER+1e-12)


def reverse_and_random(m):
    rng = np.random.default_rng(20261113)
    for n in [2, 5, 17, 101]:
        a, b = rng.uniform(LOWER, UPPER, size=(2, 7))
        expected = np.stack([a+(b-a)*(k/(n-1)) for k in range(n)])
        assert_allclose(result(m, a, b, n), expected, rtol=1e-7, atol=1e-9)
        assert_allclose(result(m, b, a, n), expected[::-1], rtol=1e-7, atol=1e-9)


def dtype_and_no_mutation(m):
    a = START.astype(np.int32)
    b = GOAL.astype(np.float32)
    before_a, before_b = a.copy(), b.copy()
    out = result(m, a, b, np.int64(7))
    expected = np.stack([a.astype(float)+(b.astype(float)-a)*(k/6) for k in range(7)])
    assert_allclose(out, expected, rtol=1e-7, atol=1e-9)
    assert_array_equal(a, before_a); assert_array_equal(b, before_b)
    assert not np.shares_memory(out, a) and not np.shares_memory(out, b)
    same = result(m, a, a, 2)
    assert not np.shares_memory(same, a)


def sample_count(m):
    for n in [0, 1, -1, 102, 10**30, 3.0, np.float32(3), True, np.bool_(False), "3", [3], None, np.array(3)]:
        with np.testing.assert_raises(ValueError):
            m.interpolate_fr3_joints(START, GOAL, n)


def shapes_and_dtypes(m):
    bad = [[], [0]*6, [0]*8, np.zeros((1, 7)), np.zeros((7, 1)), 0,
           [[0], [0, 1]], START.astype(bool), START.astype(complex), START.astype(str), START.astype(object), None]
    for value in bad:
        for index in [0, 1]:
            args = [START, GOAL, 3]; args[index] = value
            with np.testing.assert_raises(ValueError):
                m.interpolate_fr3_joints(*args)


def finite_and_limits(m):
    for index in [0, 1]:
        for j in range(7):
            for value in [np.nan, np.inf, -np.inf, LOWER[j]-1e-5, UPPER[j]+1e-5]:
                q = START.copy(); q[j] = value
                args = [START, GOAL, 3]; args[index] = q
                with np.testing.assert_raises(ValueError):
                    m.interpolate_fr3_joints(*args)


TESTS = [
    ("Three samples include the midpoint", "public", midpoint),
    ("Stationary arm still has four samples", "public", stationary),
    ("Two samples mean the two endpoints", "public", two_endpoints),
    ("All model boundaries without angle wrapping", "hidden", boundaries_and_no_wrap),
    ("Reversed and seeded seven-joint paths", "hidden", reverse_and_random),
    ("Float64 and independent storage", "hidden", dtype_and_no_mutation),
    ("Integer bounded sample count", "hidden", sample_count),
    ("Shape and dtype validation", "hidden", shapes_and_dtypes),
    ("Finite values and each joint limit", "hidden", finite_and_limits),
]
