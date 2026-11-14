import numpy as np
from numpy.testing import assert_array_equal


def same_class(m):
    out = m.class_aware_nms([[0, 0, 10, 10], [1, 1, 9, 9], [20, 20, 30, 30]], [.9, .8, .7], [0, 0, 0])
    assert out == [0, 2] and all(type(i) is int for i in out)


def different_class(m):
    assert m.class_aware_nms([[0, 0, 10, 10], [0, 0, 10, 10]], [.8, .9], [0, 1]) == [1, 0]


def empty(m):
    assert m.class_aware_nms(np.empty((0, 4)), np.empty(0), np.empty(0, dtype=int)) == []


def tie_order(m):
    boxes = [[0, 0, 2, 2], [0, 0, 2, 2], [5, 5, 6, 6], [7, 7, 8, 8]]
    assert m.class_aware_nms(boxes, [.8, .8, .8, .9], [0, 0, 0, 0]) == [3, 0, 2]


def threshold_equality(m):
    boxes = [[0, 0, 2, 2], [0, 0, 1, 2]]
    assert m.class_aware_nms(boxes, [.9, .8], [0, 0], .5) == [0, 1]
    assert m.class_aware_nms(boxes, [.9, .8], [0, 0], .499) == [0]
    assert m.class_aware_nms([boxes[0], boxes[0]], [.9, .8], [0, 0], 1.) == [0, 1]


def greedy_chain(m):
    boxes = [[0, 0, 2, 2], [1, 0, 3, 2], [2, 0, 4, 2]]
    assert m.class_aware_nms(boxes, [.9, .8, .7], [0, 0, 0], .3) == [0, 2]


def degenerate_and_touching(m):
    boxes = [[0, 0, 0, 1], [0, 0, 0, 1], [1, 0, 2, 1], [2, 0, 3, 1]]
    assert m.class_aware_nms(boxes, [.9, .8, .7, .6], [0, 0, 0, 0], 0) == [0, 1, 2, 3]


def many_classes(m):
    boxes = np.tile([0., 0, 5, 5], (12, 1)); scores = np.linspace(.1, .9, 12); classes = np.arange(12) % 3
    assert m.class_aware_nms(boxes, scores, classes) == [11, 10, 9]


def invalid_inputs(m):
    base = ([[0, 0, 2, 2]], [.9], [0])
    variants = [([[2, 0, 1, 1]], [.9], [0]), ([[0, 0, np.nan, 2]], [.9], [0]), ([[0, 0, 1e7, 2]], [.9], [0]), (base[0], [np.inf], [0]), (base[0], [1.1], [0]), (base[0], [.9], [-1]), (base[0], [.9], [.5]), (base[0], [.9], [True]), (base[0], [.9], []), ([0, 0, 1, 1], [.9], [0])]
    for boxes, scores, classes in variants:
        with np.testing.assert_raises(ValueError): m.class_aware_nms(boxes, scores, classes)
    with np.testing.assert_raises(ValueError):
        m.class_aware_nms([[0, 0, 1, 1], [2, 0, 3, 1]], [.9, .8], [True, 1])
    for threshold in [-1, 1.1, np.nan, np.inf, [.5]]:
        with np.testing.assert_raises(ValueError): m.class_aware_nms(*base, threshold)


def immutability(m):
    boxes = np.array([[0, 0, 2, 2], [0, 0, 2, 2.]]) ; scores = np.array([.8, .9]); classes = np.array([0, 0])
    before = [a.copy() for a in [boxes, scores, classes]]
    assert m.class_aware_nms(boxes, scores, classes) == [1]
    for actual, expected in zip([boxes, scores, classes], before): assert_array_equal(actual, expected)


def thousand_candidates(m):
    x = np.arange(1000) * 3.; boxes = np.stack([x, np.zeros(1000), x + 1, np.ones(1000)], axis=1)
    assert m.class_aware_nms(boxes, np.ones(1000), np.zeros(1000, dtype=int)) == list(range(1000))


TESTS = [("Same-class suppression", "public", same_class), ("Different-class overlap", "public", different_class), ("Empty candidates", "public", empty), ("Stable score ties", "hidden", tie_order), ("Strict IoU threshold", "hidden", threshold_equality), ("Greedy chain semantics", "hidden", greedy_chain), ("Zero-area and touching boxes", "hidden", degenerate_and_touching), ("Many classes and global score order", "hidden", many_classes), ("Invalid inputs", "hidden", invalid_inputs), ("Input immutability", "hidden", immutability), ("Thousand candidate scale", "hidden", thousand_candidates)]
