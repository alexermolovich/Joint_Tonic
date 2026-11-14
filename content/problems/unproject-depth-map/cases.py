import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def small_image(m):
    out, valid = m.unproject_depth([[1, 2], [0, 4]], [[2, 0, 0], [0, 2, 0], [0, 0, 1]])
    assert_allclose(out, [[0, 0, 1], [1, 0, 2], [np.nan] * 3, [2, 2, 4]], equal_nan=True)
    assert_array_equal(valid, [True, True, False, True])


def principal_point(m):
    out, valid = m.unproject_depth([[2, np.nan]], [[4, 0, 1], [0, 2, 0], [0, 0, 1]])
    assert_allclose(out, [[-.5, 0, 2], [np.nan] * 3], equal_nan=True)
    assert_array_equal(valid, [True, False])


def all_missing(m):
    out, valid = m.unproject_depth([[0, -1, np.nan, np.inf, -np.inf]], np.eye(3))
    assert np.isnan(out).all()
    assert not valid.any()


def empty_and_dtypes(m):
    for shape in [(0, 4), (4, 0), (0, 0)]:
        out, valid = m.unproject_depth(np.empty(shape, np.float32), np.eye(3))
        assert out.shape == (0, 3) and valid.shape == (0,)
        assert out.dtype == np.float64 and valid.dtype == np.bool_
    out, valid = m.unproject_depth(np.ones((1, 1), np.int32), np.eye(3, dtype=np.int32))
    assert out.dtype == np.float64 and valid.dtype == np.bool_


def calibration(m):
    for position, value in [((0, 0), 0), ((1, 1), -1), ((0, 1), .1), ((1, 0), .1),
                            ((2, 0), .01), ((2, 2), 2), ((0, 2), np.inf),
                            ((0, 0), 1e-7), ((0, 2), 1000001)]:
        K = np.eye(3); K[position] = value
        with np.testing.assert_raises(ValueError):
            m.unproject_depth([[1]], K)
    K = np.eye(3); K[0, 1] = 1e-9
    out, valid = m.unproject_depth([[1]], K)
    assert_allclose(out, [[0, 0, 1]])
    assert valid[0]


def malformed(m):
    for bad in [[], [1, 2], np.zeros((1, 1, 1)), [[1j]], [["1"]], [[True]], [[1000001]], np.array([[1]], object)]:
        with np.testing.assert_raises(ValueError):
            m.unproject_depth(bad, np.eye(3))
    for K in [np.eye(2), np.ones((3, 3), bool), np.eye(3).astype(complex), np.eye(3).astype(str)]:
        with np.testing.assert_raises(ValueError):
            m.unproject_depth([[1]], K)


def round_trip_scale(m):
    rng = np.random.default_rng(20261113)
    depth = rng.uniform(.1, 10, (128, 192)).astype(np.float32)
    K = np.array([[120., 0, 73], [0, 175, 61], [0, 0, 1]])
    before, kb = depth.copy(), K.copy()
    out, valid = m.unproject_depth(depth, K)
    assert out.shape == (depth.size, 3) and valid.all()
    # Independent projection round trip recovers the original integer pixels.
    pixels = out[:, :2] / out[:, 2, None] * [120, 175] + [73, 61]
    v, u = np.indices(depth.shape)
    assert_allclose(pixels, np.column_stack([u.ravel(), v.ravel()]), atol=1e-9)
    assert_allclose(out[:, 2], depth.ravel())
    assert_array_equal(depth, before); assert_array_equal(K, kb)
    assert not np.shares_memory(out, depth) and not np.shares_memory(out, K)


TESTS = [("Row-major point cloud", "public", small_image), ("Principal point", "public", principal_point),
         ("Missing depth policy", "hidden", all_missing), ("Empty shapes and dtype", "hidden", empty_and_dtypes),
         ("Calibration form and tolerance", "hidden", calibration), ("Malformed inputs", "hidden", malformed),
         ("Projection round trip and preservation", "hidden", round_trip_scale)]
