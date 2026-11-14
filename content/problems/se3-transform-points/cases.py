import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def identity(m):
    out = m.transform_points(np.eye(4), [1, 2, 3])
    assert isinstance(out, np.ndarray) and out.shape == (3,) and out.dtype == np.float64
    assert_allclose(out, [1, 2, 3])


def translation(m):
    T = np.eye(4); T[:3, 3] = [1, -2, 3]
    assert_allclose(m.transform_points(T, [[0, 0, 0], [2, 1, -1]]), [[1, -2, 3], [3, -1, 2]])


def rotation(m):
    T = np.array([[0, -1, 0, 1], [1, 0, 0, 2], [0, 0, 1, 0], [0, 0, 0, 1]])
    assert_allclose(m.transform_points(T, [1, 0, 0]), [1, 3, 0])


def composition(m):
    A = np.eye(4); A[:3, 3] = [2, -4, 1]
    B = np.array([[0, -1, 0, 1], [1, 0, 0, 0], [0, 0, 1, -2], [0, 0, 0, 1.]])
    p = np.random.default_rng(20261113).normal(size=(43, 3))
    assert_allclose(m.transform_points(A @ B, p), m.transform_points(A, m.transform_points(B, p)), atol=1e-9)


def inverse_round_trip(m):
    angle = .71; c, s = np.cos(angle), np.sin(angle)
    T = np.array([[c, -s, 0, 3], [s, c, 0, -2], [0, 0, 1, 4], [0, 0, 0, 1.]])
    p = np.array([[1, 2, 3], [-2, .1, 4]])
    assert_allclose(m.transform_points(np.linalg.inv(T), m.transform_points(T, p)), p, atol=1e-9)


def empty_batch(m):
    out = m.transform_points(np.eye(4), np.empty((0, 3)))
    assert out.shape == (0, 3) and out.dtype == np.float64


def immutability_and_dtype(m):
    T = np.eye(4, dtype=np.float32); p = np.array([[1, 2, 3]], dtype=np.int32)
    Tc, pc = T.copy(), p.copy(); out = m.transform_points(T, p)
    assert out.dtype == np.float64 and not np.shares_memory(out, p) and not np.shares_memory(out, T)
    assert_array_equal(T, Tc); assert_array_equal(p, pc)


def invalid_shapes(m):
    for T, p in [(np.eye(3), [1, 2, 3]), (np.eye(4), [1, 2]), (np.eye(4), []), (np.eye(4), np.zeros((2, 3, 1)))]:
        with np.testing.assert_raises(ValueError): m.transform_points(T, p)


def invalid_rigid_transforms(m):
    for T in [np.diag([2., 1, 1, 1]), np.diag([-1., 1, 1, 1]), np.eye(4)]:
        if np.array_equal(T, np.eye(4)): T[3, 0] = .01
        with np.testing.assert_raises(ValueError): m.transform_points(T, [0, 0, 0])


def nonfinite(m):
    for bad in [np.nan, np.inf]:
        with np.testing.assert_raises(ValueError): m.transform_points(np.eye(4), [bad, 0, 0])
        T = np.eye(4); T[0, 3] = bad
        with np.testing.assert_raises(ValueError): m.transform_points(T, [0, 0, 0])


def large_batch(m):
    p = np.random.default_rng(72).normal(size=(100_000, 3)); T = np.eye(4); T[:3, 3] = [2, 3, -1]
    assert_allclose(m.transform_points(T, p), p + [2, 3, -1], atol=1e-9)


TESTS = [("Identity and output shape", "public", identity), ("Translation", "public", translation), ("Rotation then translation", "public", rotation), ("Transform composition", "hidden", composition), ("Inverse round trip", "hidden", inverse_round_trip), ("Empty batch", "hidden", empty_batch), ("Input immutability and dtype", "hidden", immutability_and_dtype), ("Invalid shapes", "hidden", invalid_shapes), ("Invalid rigid transforms", "hidden", invalid_rigid_transforms), ("Nonfinite values", "hidden", nonfinite), ("Large batch", "hidden", large_batch)]
