import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

K = np.array([[100., 0, 50], [0, 100, 40], [0, 0, 1]])


def optical_axis(m):
    p, d, v = m.project_points([[0, 0, 2]], K, (100, 80))
    assert_allclose(p, [[50, 40]]); assert_allclose(d, [2]); assert_array_equal(v, [True])
    assert p.dtype == d.dtype == np.float64 and v.dtype == np.bool_


def off_axis(m):
    p, d, v = m.project_points([[.2, -.4, 2]], K, (100, 80))
    assert_allclose(p, [[60, 20]]); assert_array_equal(v, [True])


def behind_camera(m):
    p, d, v = m.project_points([[0, 0, -1]], K, (100, 80))
    assert np.isnan(p).all(); assert_allclose(d, [-1]); assert_array_equal(v, [False])


def depth_epsilon(m):
    p, d, v = m.project_points([[0, 0, 0], [0, 0, 1e-8], [0, 0, 1.0001e-8]], K, (100, 80))
    assert np.isnan(p[:2]).all(); assert_allclose(p[2], [50, 40]); assert_array_equal(v, [False, False, True])


def image_boundaries(m):
    points = [[-.5, -.4, 1], [.5, 0, 1], [0, .4, 1], [-.5001, 0, 1], [0, -.4001, 1]]
    p, d, v = m.project_points(points, K, (100, 80))
    assert_allclose(p[:3], [[0, 0], [100, 40], [50, 80]]); assert_array_equal(v, [True, False, False, False, False])


def empty_batch(m):
    p, d, v = m.project_points(np.empty((0, 3)), K, (100, 80))
    assert p.shape == (0, 2) and d.shape == v.shape == (0,)


def anisotropic_intrinsics(m):
    k = np.array([[40., 0, 10], [0, 70, 20], [0, 0, 1]])
    p, d, v = m.project_points([[2, 1, 2]], k, (90, 60))
    assert_allclose(p, [[50, 55]]); assert_array_equal(v, [True])


def invalid_intrinsics(m):
    variants = [np.eye(2), K.copy(), K.copy(), K.copy()]
    variants[1][0, 0] = 0; variants[2][0, 1] = 1; variants[3][2, 2] = 2
    for k in variants:
        with np.testing.assert_raises(ValueError): m.project_points([[0, 0, 1]], k, (100, 80))


def invalid_inputs(m):
    for size in [(0, 80), (100, -1), (100., 80.), (True, False), (True, 80), (100,)]:
        with np.testing.assert_raises(ValueError): m.project_points([[0, 0, 1]], K, size)
    for p in [[0, 0, 1], [[0, np.nan, 1]], [[0, 0, np.inf]], np.zeros((1, 2))]:
        with np.testing.assert_raises(ValueError): m.project_points(p, K, (100, 80))


def immutability(m):
    p = np.array([[.2, .1, 2.]]) ; pc = p.copy(); kc = K.copy()
    pixels, depths, v = m.project_points(p, K, (100, 80))
    assert not np.shares_memory(pixels, p) and not np.shares_memory(depths, p)
    assert_array_equal(p, pc); assert_array_equal(K, kc)


def large_batch(m):
    rng = np.random.default_rng(20261113); p = rng.normal(size=(100_000, 3)); p[:, 2] = np.abs(p[:, 2]) + .1
    pixels, d, v = m.project_points(p, K, (100, 80))
    assert_allclose(pixels, p[:, :2] / p[:, 2, None] * [100, 100] + [50, 40], atol=1e-9)
    assert_array_equal(v, (pixels[:, 0] >= 0) & (pixels[:, 0] < 100) & (pixels[:, 1] >= 0) & (pixels[:, 1] < 80))


TESTS = [("Optical axis", "public", optical_axis), ("Off-axis point", "public", off_axis), ("Behind camera", "public", behind_camera), ("Depth threshold", "hidden", depth_epsilon), ("Half-open image boundaries", "hidden", image_boundaries), ("Empty batch", "hidden", empty_batch), ("Independent focal lengths", "hidden", anisotropic_intrinsics), ("Invalid calibration", "hidden", invalid_intrinsics), ("Invalid inputs", "hidden", invalid_inputs), ("Input immutability", "hidden", immutability), ("Large vectorized batch", "hidden", large_batch)]
