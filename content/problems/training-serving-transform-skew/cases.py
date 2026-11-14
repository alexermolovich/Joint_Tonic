import numpy as np


def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")


def absolute_boundary(m):
    train = np.array([[1., 0.], [2., .5]])
    serve = np.array([[1.125, .25], [2.5, .625]])
    assert m.transform_skew(train, serve, ["depth_m", "yaw_rad"], np.array([.125, .125])) == [(0, "yaw_rad"), (1, "depth_m")]


def relative_zero(m):
    assert m.transform_skew(np.array([[8., 0.]]), np.array([[9., .25]]),
                            ["depth_m", "yaw_rad"], np.array([0., .125]), .125) == [(0, "yaw_rad")]


def empty(m):
    assert m.transform_skew(np.empty((0, 2)), np.empty((0, 2)), ["a", "b"], np.zeros(2)) == []
    assert m.transform_skew(np.empty((3, 0)), np.empty((3, 0)), [], np.empty(0)) == []


def asymmetric(m):
    assert m.transform_skew(np.array([[1.]]), np.array([[2.]]), ["x"], np.zeros(1), .5) == [(0, "x")]
    assert m.transform_skew(np.array([[2.]]), np.array([[1.]]), ["x"], np.zeros(1), .5) == []


def order_and_immutability(m):
    train = np.zeros((2, 2))
    serve = np.ones((2, 2))
    names = ["z", "a"]
    tolerance = np.zeros(2)
    before = [value.copy() for value in (train, serve, tolerance)]
    result = m.transform_skew(train, serve, names, tolerance)
    assert type(result) is list and result == [(0, "z"), (0, "a"), (1, "z"), (1, "a")]
    assert all(type(row) is int and type(name) is str for row, name in result)
    for actual, expected in zip((train, serve, tolerance), before):
        assert np.array_equal(actual, expected)
    assert names == ["z", "a"]


def noncontiguous_and_scale(m):
    train = np.arange(24., dtype=np.float64).reshape(4, 6)[:, ::2]
    serve = train.copy()
    serve[2, 1] += 1
    assert m.transform_skew(train, serve, ["a", "b", "c"], np.zeros(3)) == [(2, "b")]
    large = np.zeros((10000, 128))
    changed = large.copy()
    changed[-1, -1] = 1
    assert m.transform_skew(large, changed, ["f" + str(i) for i in range(128)], np.zeros(128)) == [(9999, "f127")]


def invalid_arrays(m):
    good = np.zeros((1, 1))
    for args in [
        ([], good, ["x"], np.zeros(1)),
        (good.astype(np.float32), good, ["x"], np.zeros(1)),
        (good, np.zeros((2, 1)), ["x"], np.zeros(1)),
        (good, good, ["x"], np.zeros((1, 1))),
        (good, good, ["x"], np.zeros(1, dtype=np.float32)),
        (good, good, ["x"], np.array([-1.])),
        (good, good, [""], np.zeros(1)),
        (good, good, np.array(["x"]), np.zeros(1)),
        (good, good, [["x"]], np.zeros(1)),
        (np.zeros((1, 2)), np.zeros((1, 2)), ["x", "x"], np.zeros(2)),
    ]:
        invalid(lambda args=args: m.transform_skew(*args))
    for bad in [np.nan, np.inf, -np.inf, 1e101]:
        invalid(lambda bad=bad: m.transform_skew(np.array([[bad]]), good, ["x"], np.zeros(1)))
        invalid(lambda bad=bad: m.transform_skew(good, good, ["x"], np.array([bad])))


def invalid_scalars_and_limits(m):
    good = np.zeros((1, 1))
    for bad in [True, -1., 1.1, float("nan"), float("inf"), "0", np.float64(0), 10**1000]:
        invalid(lambda bad=bad: m.transform_skew(good, good, ["x"], np.zeros(1), bad))
    invalid(lambda: m.transform_skew(np.zeros((10001, 0)), np.zeros((10001, 0)), [], np.zeros(0)))
    invalid(lambda: m.transform_skew(np.zeros((0, 129)), np.zeros((0, 129)), ["f" + str(i) for i in range(129)], np.zeros(129)))


TESTS = [
    ("Absolute tolerance equality", "public", absolute_boundary),
    ("Relative tolerance and a zero feature", "public", relative_zero),
    ("Empty rows and feature columns", "public", empty),
    ("Training-side relative reference", "hidden", asymmetric),
    ("Row-major reporting and immutability", "hidden", order_and_immutability),
    ("Noncontiguous and maximum shape", "hidden", noncontiguous_and_scale),
    ("Invalid arrays, names, and tolerances", "hidden", invalid_arrays),
    ("Scalar types and declared bounds", "hidden", invalid_scalars_and_limits),
]
