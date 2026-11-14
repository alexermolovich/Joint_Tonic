import math
import numpy as np
from numpy.testing import assert_array_equal, assert_allclose


def weighted(m):
    p = np.array([[[0.], [0.], [2.]], [[0.], [4.], [0.]], [[8.], [0.], [0.]]])
    a, w = m.temporal_ensemble(p, np.array([0, 1, 2], dtype=np.int64), np.ones((3, 3), dtype=bool), 2, math.log(2))
    assert_allclose(a, [24 / 7]); assert_allclose(w, [4 / 7, 2 / 7, 1 / 7])
    assert a.dtype == w.dtype == np.float64


def zero_action(m):
    p = np.array([[[7.], [7.], [0.]], [[10.], [20.], [30.]]], dtype=np.float32)
    a, w = m.temporal_ensemble(p, np.array([5, 7], dtype=np.int64), np.ones((2, 3), dtype=bool), 7, 0)
    assert_allclose(a, [5]); assert_allclose(w, [.5, .5])
    assert a.dtype == w.dtype == np.float32


def eligible_ranks(m):
    p = np.ones((5, 10, 1), dtype=np.float64)
    p[0] = 2; p[1] = 100; p[2] = 4; p[3] = 1000; p[4] = -500
    valid = np.ones((5, 10), dtype=bool); valid[1] = False
    a, w = m.temporal_ensemble(p, np.array([1, 2, 8, 11, 12], dtype=np.int64), valid, 9, math.log(2))
    assert_allclose(a, [8 / 3]); assert_allclose(w, [2 / 3, 0, 1 / 3, 0, 0])
    a, w = m.temporal_ensemble(p, np.array([1, 2, 8, 11, 12], dtype=np.int64), valid, 11, 0)
    assert_allclose(a, [502]); assert_allclose(w, [0, 0, .5, .5, 0])


def stability(m):
    p = np.arange(128., dtype=np.float64)[:, None, None] + np.zeros((128, 128, 2))
    a, w = m.temporal_ensemble(p, np.arange(128, dtype=np.int64), np.ones((128, 128), dtype=bool), 127, 100)
    assert np.isfinite(a).all() and np.isfinite(w).all()
    assert_allclose(w.sum(), 1); assert_allclose(a, [0, 0], atol=1e-40)
    assert w[0] == 1


def noncontiguous(m):
    p = np.arange(48., dtype=np.float64).reshape(3, 4, 4)[:, :, ::2]
    ticks = np.array([0, 99, 1, 99, 2], dtype=np.int64)[::2]
    valid = np.ones((3, 8), dtype=bool)[:, ::2]
    before = [x.copy() for x in (p, ticks, valid)]
    a, w = m.temporal_ensemble(p, ticks, valid, 2, 0)
    assert_allclose(a, (p[0, 2] + p[1, 1] + p[2, 0]) / 3)
    for x, y in zip((p, ticks, valid), before): assert_array_equal(x, y)
    assert not np.shares_memory(a, p) and not np.shares_memory(w, p)


def expect(error, fn):
    try:
        fn()
    except error:
        return
    raise AssertionError("expected " + error.__name__)


def no_eligible(m):
    expect(ValueError, lambda: m.temporal_ensemble(np.zeros((0, 2, 1)), np.array([], dtype=np.int64), np.zeros((0, 2), dtype=bool), 0, 0))
    p, t, v = np.zeros((1, 2, 1)), np.array([3], dtype=np.int64), np.ones((1, 2), dtype=bool)
    for tick in (2, 5):
        expect(ValueError, lambda tick=tick: m.temporal_ensemble(p, t, v, tick, 0))
    expect(ValueError, lambda: m.temporal_ensemble(p, t, ~v, 3, 0))


def contracts(m):
    p, t, v = np.zeros((2, 2, 1)), np.array([0, 1], dtype=np.int64), np.ones((2, 2), dtype=bool)
    for index in range(3):
        args = [p, t, v, 1, 0]; args[index] = args[index].tolist()
        expect(TypeError, lambda args=args: m.temporal_ensemble(*args))
    for bad in (True, 1., np.int64(1)):
        expect(TypeError, lambda bad=bad: m.temporal_ensemble(p, t, v, bad, 0))
    for bad in (True, np.float64(1), "1"):
        expect(TypeError, lambda bad=bad: m.temporal_ensemble(p, t, v, 1, bad))
    for bad in (-1, 101, 10**1000, float("nan"), float("inf")):
        expect(ValueError, lambda bad=bad: m.temporal_ensemble(p, t, v, 1, bad))
    for bad in (t.astype(np.int32), np.array([0, 0], dtype=np.int64), np.array([2, 1], dtype=np.int64), np.array([-1, 1], dtype=np.int64)):
        expect(ValueError, lambda bad=bad: m.temporal_ensemble(p, bad, v, 1, 0))
    for bad in (p.astype(int), p[0], np.full_like(p, np.nan), np.full_like(p, 1e6 + 1)):
        expect(ValueError, lambda bad=bad: m.temporal_ensemble(bad, t, v, 1, 0))
    expect(ValueError, lambda: m.temporal_ensemble(p, t, v.astype(int), 1, 0))


TESTS = [
    ("Oldest-first weighted blend", "public", weighted),
    ("Zero is a valid action", "public", zero_action),
    ("Eligibility, gaps and compact ranks", "hidden", eligible_ranks),
    ("Large decay and chunk count", "hidden", stability),
    ("Noncontiguous arrays and immutability", "hidden", noncontiguous),
    ("No eligible prediction", "hidden", no_eligible),
    ("Scalar and array contracts", "hidden", contracts),
]
