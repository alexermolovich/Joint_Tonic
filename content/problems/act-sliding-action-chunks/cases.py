import numpy as np
from numpy.testing import assert_array_equal


def tail(m):
    chunks, valid = m.sliding_action_chunks(np.array([[1.], [2.], [3.]]), np.array([0, 2], dtype=np.int64), 2)
    assert_array_equal(chunks, [[[1], [2]], [[3], [0]]])
    assert_array_equal(valid, [[True, True], [True, False]])
    assert chunks.dtype == np.float64 and valid.dtype == np.bool_


def repeated(m):
    chunks, valid = m.sliding_action_chunks(np.array([[2., -1.], [4., 3.]], dtype=np.float32), np.array([1, 0, 1], dtype=np.int64), 3)
    assert_array_equal(chunks, [[[4, 3], [0, 0], [0, 0]], [[2, -1], [4, 3], [0, 0]], [[4, 3], [0, 0], [0, 0]]])
    assert_array_equal(valid, [[1, 0, 0], [1, 1, 0], [1, 0, 0]])
    assert chunks.dtype == np.float32


def empty_and_zero(m):
    actions = np.zeros((2, 3), dtype=np.float32)
    chunks, valid = m.sliding_action_chunks(actions, np.array([], dtype=np.int64), 4)
    assert chunks.shape == (0, 4, 3) and valid.shape == (0, 4)
    chunks, valid = m.sliding_action_chunks(actions, np.array([1], dtype=np.int64), 2)
    assert_array_equal(chunks, np.zeros((1, 2, 3)))
    assert_array_equal(valid, [[True, False]])


def noncontiguous(m):
    actions = np.arange(60., dtype=np.float64).reshape(10, 6)[:, ::2]
    starts = np.array([9, 7, 3, 1], dtype=np.int64)[::2]
    before, start_before = actions.copy(), starts.copy()
    chunks, valid = m.sliding_action_chunks(actions, starts, 3)
    expected = np.zeros((2, 3, 3))
    expected[0, 0] = actions[9]
    expected[1] = actions[3:6]
    assert_array_equal(chunks, expected)
    assert_array_equal(valid, [[1, 0, 0], [1, 1, 1]])
    assert_array_equal(actions, before); assert_array_equal(starts, start_before)
    assert not np.shares_memory(chunks, actions) and not np.shares_memory(valid, starts)


def scale(m):
    actions = np.arange(10000., dtype=np.float32)[:, None]
    starts = np.arange(0, 10000, 5, dtype=np.int64)
    chunks, valid = m.sliding_action_chunks(actions, starts, 64)
    assert chunks.shape == (2000, 64, 1)
    assert_array_equal(chunks[100, :, 0], np.arange(500, 564))
    assert valid[-1].sum() == 5 and np.all(chunks[-1, 5:] == 0)


def expect(error, fn):
    try:
        fn()
    except error:
        return
    raise AssertionError("expected " + error.__name__)


def types(m):
    a, s = np.zeros((2, 1)), np.array([0], dtype=np.int64)
    expect(TypeError, lambda: m.sliding_action_chunks(a.tolist(), s, 1))
    expect(TypeError, lambda: m.sliding_action_chunks(a, s.tolist(), 1))
    for h in (True, 1., np.int64(1), "1"):
        expect(TypeError, lambda h=h: m.sliding_action_chunks(a, s, h))


def contracts(m):
    a, s = np.zeros((2, 1)), np.array([0], dtype=np.int64)
    for bad in (np.zeros((0, 1)), np.zeros((2, 0)), a.astype(np.int32), a[0], np.full_like(a, np.nan), np.full_like(a, 1e6 + 1)):
        expect(ValueError, lambda bad=bad: m.sliding_action_chunks(bad, s, 1))
    for bad in (s.astype(np.int32), s.astype(float), s[:, None], np.array([-1], dtype=np.int64), np.array([2], dtype=np.int64)):
        expect(ValueError, lambda bad=bad: m.sliding_action_chunks(a, bad, 1))
    for h in (0, -1, 257):
        expect(ValueError, lambda h=h: m.sliding_action_chunks(a, s, h))
    expect(ValueError, lambda: m.sliding_action_chunks(np.zeros((1, 64)), np.zeros(4096, dtype=np.int64), 256))


TESTS = [
    ("Complete chunk and episode tail", "public", tail),
    ("Unsorted repeated starts", "public", repeated),
    ("Empty requests and valid zero actions", "hidden", empty_and_zero),
    ("Noncontiguous inputs and ownership", "hidden", noncontiguous),
    ("Realistic trajectory length", "hidden", scale),
    ("Argument types", "hidden", types),
    ("Bounds, values and shape validation", "hidden", contracts),
]
