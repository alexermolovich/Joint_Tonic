import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def identical(m):
    out = m.pairwise_iou([[0, 0, 2, 2]], [[0, 0, 2, 2]])
    assert out.shape == (1, 1) and out.dtype == np.float64; assert_allclose(out, [[1]])


def disjoint(m):
    assert_allclose(m.pairwise_iou([[0, 0, 1, 1]], [[2, 2, 3, 3], [1, 0, 2, 1]]), [[0, 0]])


def partial_overlap(m):
    assert_allclose(m.pairwise_iou([[0, 0, 2, 2]], [[1, 1, 3, 3], [0, 0, 1, 1]]), [[1 / 7, 1 / 4]])


def empty_sets(m):
    empty = np.empty((0, 4)); one = [[0, 0, 1, 1]]
    assert m.pairwise_iou(empty, one).shape == (0, 1)
    assert m.pairwise_iou(one, empty).shape == (1, 0)
    assert m.pairwise_iou(empty, empty).shape == (0, 0)


def zero_area(m):
    z = [[0, 0, 0, 2], [1, 1, 1, 1]]
    assert_allclose(m.pairwise_iou(z, z + [[0, 0, 2, 2]]), np.zeros((2, 3)))


def pair_axes_and_symmetry(m):
    a = np.array([[0, 0, 2, 2], [0, 0, 4, 4.]])
    b = np.array([[0, 0, 1, 1], [2, 2, 4, 4], [8, 8, 9, 9.]])
    expected = [[.25, 0, 0], [1 / 16, .25, 0]]
    assert_allclose(m.pairwise_iou(a, b), expected)
    assert_allclose(m.pairwise_iou(a, b), m.pairwise_iou(b, a).T)


def translation_and_scale(m):
    a = np.array([[-2, 1, 3, 6.], [0, 0, 4, 2.]])
    b = np.array([[1, 2, 5, 7.]])
    expected = m.pairwise_iou(a, b)
    shift = np.array([50, -3, 50, -3])
    assert_allclose(m.pairwise_iou(a * 10 + shift, b * 10 + shift), expected)
    assert_allclose(expected[0, 0], 8 / (25 + 20 - 8))


def invalid_boxes(m):
    for bad in [[[2, 0, 1, 1]], [[0, 2, 1, 1]], [[0, 0, np.inf, 1]], [[0, 0, np.nan, 1]], [[0, 0, 1e7, 1]], [0, 0, 1, 1], []]:
        with np.testing.assert_raises(ValueError): m.pairwise_iou(bad, [[0, 0, 1, 1]])
        with np.testing.assert_raises(ValueError): m.pairwise_iou([[0, 0, 1, 1]], bad)


def immutability(m):
    a = np.array([[0, 0, 2, 2]], dtype=np.int32); b = a.copy(); ac = a.copy(); bc = b.copy()
    out = m.pairwise_iou(a, b)
    assert_array_equal(a, ac); assert_array_equal(b, bc); assert not np.shares_memory(out, a) and not np.shares_memory(out, b)


def matrix_scale(m):
    rng = np.random.default_rng(20261113); xy = rng.uniform(0, 100, (400, 2)); wh = rng.uniform(.1, 10, (400, 2)); a = np.concatenate([xy, xy + wh], axis=1)
    out = m.pairwise_iou(a, a)
    assert out.shape == (400, 400); assert_allclose(np.diag(out), 1); assert_allclose(out, out.T); assert np.all((out >= 0) & (out <= 1))


TESTS = [("Identical boxes", "public", identical), ("Disjoint and touching boxes", "public", disjoint), ("Partial overlap and containment", "public", partial_overlap), ("Empty sets preserve axes", "hidden", empty_sets), ("Zero-area boxes", "hidden", zero_area), ("Pair axes and symmetry", "hidden", pair_axes_and_symmetry), ("Translation and scale invariance", "hidden", translation_and_scale), ("Invalid box contract", "hidden", invalid_boxes), ("Input immutability", "hidden", immutability), ("Pairwise matrix scale", "hidden", matrix_scale)]
