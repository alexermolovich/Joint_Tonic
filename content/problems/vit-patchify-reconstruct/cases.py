import numpy as np
from numpy.testing import assert_array_equal


def rectangular(m):
    x = np.array([[[[1, 2, 3, 4], [5, 6, 7, 8]]]], dtype=np.float32)
    z = m.patchify(x, 2)
    assert_array_equal(z, [[[1, 2, 5, 6], [3, 4, 7, 8]]])
    assert z.dtype == x.dtype
    assert_array_equal(m.unpatchify(z, x.shape, 2), x)


def channels(m):
    x = np.array([[[[1, 2], [3, 4]], [[10, 20], [30, 40]]]], dtype=np.float64)
    assert_array_equal(m.patchify(x, 2), [[[1, 2, 3, 4, 10, 20, 30, 40]]])


def one_pixel(m):
    x = np.arange(12, dtype=np.float64).reshape(1, 2, 2, 3)
    z = m.patchify(x, 1)
    assert_array_equal(z, [[[0, 6], [1, 7], [2, 8], [3, 9], [4, 10], [5, 11]]])
    assert_array_equal(m.unpatchify(z, x.shape, 1), x)


def general_layout(m):
    x = np.arange(2*3*6*8, dtype=np.float32).reshape(2, 3, 6, 8)[:, :, ::-1, ::-1]
    z = m.patchify(x, 2)
    expected = np.stack([np.stack([image[:, r:r+2, c:c+2].ravel() for r in range(0, 6, 2) for c in range(0, 8, 2)]) for image in x])
    assert_array_equal(z, expected)
    assert_array_equal(m.unpatchify(z[:, ::-1, :][:, ::-1, :], x.shape, 2), x)


def empty(m):
    x = np.empty((0, 3, 4, 6), dtype=np.float64)
    z = m.patchify(x, 2)
    assert z.shape == (0, 6, 12)
    assert m.unpatchify(z, x.shape, 2).shape == x.shape


def ownership(m):
    x = np.arange(16, dtype=np.float64).reshape(1, 1, 4, 4)
    old = x.copy()
    z = m.patchify(x, 4)
    y = m.unpatchify(z, x.shape, 4)
    assert not np.shares_memory(x, z) and not np.shares_memory(z, y)
    assert_array_equal(x, old)
    z[...] = -1
    assert_array_equal(y, old)


def bad_inputs(m):
    with np.testing.assert_raises(TypeError): m.patchify([[[[1.]]]], 1)
    with np.testing.assert_raises(TypeError): m.unpatchify([], (0, 1, 1, 1), 1)
    for x, p in [(np.ones((1,1,3,4)),2), (np.ones((1,1,2,2)),True), (np.ones((1,1,2,2)),0), (np.ones((1,1,2,2),dtype=int),1), (np.full((1,1,1,1),np.nan),1), (np.empty((0,0,2,2)),1), (np.ones((1,2,2)),1), (np.empty((0,1,5000,2)),1)]:
        with np.testing.assert_raises(ValueError): m.patchify(x,p)
    for shape in [(1,1,2,3), [1,1,2,2], (True,1,2,2), (0,0,2,2)]:
        with np.testing.assert_raises(ValueError): m.unpatchify(np.ones((1,1,4)),shape,2)


def scale(m):
    rng = np.random.default_rng(20261113)
    x = rng.normal(size=(4, 3, 128, 128)).astype(np.float32)
    z = m.patchify(x, 16)
    assert z.shape == (4,64,768)
    assert_array_equal(m.unpatchify(z, x.shape, 16), x)


TESTS = [("Rectangular image", "public", rectangular), ("Channel ordering", "public", channels),
         ("One-pixel patches", "public", one_pixel), ("General layout", "hidden", general_layout),
         ("Empty batch", "hidden", empty), ("Independent storage", "hidden", ownership),
         ("Validation", "hidden", bad_inputs), ("Realistic batch", "hidden", scale)]
