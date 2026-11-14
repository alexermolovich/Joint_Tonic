import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def assert_record(actual, box, class_id, score):
    assert isinstance(actual, dict) and set(actual) == {"box", "class_id", "score"}
    assert isinstance(actual["box"], list) and all(type(v) is float for v in actual["box"])
    assert type(actual["class_id"]) is int and type(actual["score"]) is float
    assert_allclose(actual["box"], box, atol=1e-9); assert actual["class_id"] == class_id; assert_allclose(actual["score"], score)


def single_cell(m):
    p = np.array([[[[.5, .5, .4, .5, .8, .75]]]])
    out = m.decode_yolo(p, (100, 80)); assert isinstance(out, list) and len(out) == 1
    assert_record(out[0], [30, 20, 70, 60], 0, .6)


def multiple_classes(m):
    p = np.array([[[[.5, .5, .4, .5, .8, .75, .5]]]])
    out = m.decode_yolo(p, (100, 80), .4); assert len(out) == 2
    assert_record(out[0], [30, 20, 70, 60], 0, .6); assert_record(out[1], [30, 20, 70, 60], 1, .4)


def filtered_empty(m):
    p = np.array([[[[.5, .5, .4, .5, .2, .75]]]])
    assert m.decode_yolo(p, (100, 80)) == []


def rectangular_grid(m):
    p = np.zeros((2, 4, 1, 6)); p[1, 2, 0] = [.25, .5, .2, .4, .8, .5]
    out = m.decode_yolo(p, (200, 100)); assert len(out) == 1
    assert_record(out[0], [92.5, 55, 132.5, 95], 0, .4)


def clipping(m):
    p = np.array([[[[0., 1., .6, .6, 1., 1.]]]])
    out = m.decode_yolo(p, (100, 50)); assert len(out) == 1
    assert_record(out[0], [0, 35, 30, 50], 0, 1.)


def deterministic_ties(m):
    p = np.zeros((1, 2, 2, 7)); p[..., 0:2] = .5; p[..., 2:4] = .2; p[..., 4:] = 1
    out = m.decode_yolo(p, (100, 100)); assert len(out) == 8
    assert [r["class_id"] for r in out] == [0, 1] * 4
    assert_allclose([r["box"][0] for r in out], [15] * 4 + [65] * 4)


def score_order(m):
    p = np.array([[[[.25, .5, .2, .2, .8, .5]], [[.5, .5, .2, .2, 1., .9]]]])
    out = m.decode_yolo(p, (100, 100)); assert len(out) == 2
    assert_allclose([r["score"] for r in out], [.9, .4]); assert_allclose(out[0]["box"], [65, 40, 85, 60])


def inclusive_zero_and_empty_area(m):
    p = np.array([[[[.5, .5, .2, .2, 0., 1.], [.5, .5, 0., .2, 1., 1.]]]])
    out = m.decode_yolo(p, (100, 100), 0); assert len(out) == 1
    assert_record(out[0], [40, 40, 60, 60], 0, 0.)
    p[0, 0, 0, 4] = .5
    assert len(m.decode_yolo(p, (100, 100), .5)) == 1


def invalid_prediction(m):
    for p in [np.zeros((1, 1, 6)), np.zeros((1, 1, 1, 5)), np.zeros((0, 1, 1, 6)), np.full((1, 1, 1, 6), np.nan), np.full((1, 1, 1, 6), 1.1), np.full((1, 1, 1, 6), -.1)]:
        with np.testing.assert_raises(ValueError): m.decode_yolo(p, (100, 100))


def invalid_size_threshold(m):
    p = np.array([[[[.5, .5, .2, .2, 1., 1.]]]])
    for size in [(0, 100), (100., 100.), (True, False), (True, 100), (100,)]:
        with np.testing.assert_raises(ValueError): m.decode_yolo(p, size)
    for t in [-.1, 1.1, np.nan, np.inf, [.5]]:
        with np.testing.assert_raises(ValueError): m.decode_yolo(p, (100, 100), t)


def immutability(m):
    p = np.array([[[[.5, .5, .2, .2, 1., .8, .8]]]]); before = p.copy()
    out = m.decode_yolo(p, (100, 100)); out[0]["box"][0] = -99
    assert_array_equal(p, before); assert out[1]["box"][0] == 40


TESTS = [("Single cell", "public", single_cell), ("Per-class score products", "public", multiple_classes), ("All predictions filtered", "public", filtered_empty), ("Rectangular image and grid", "hidden", rectangular_grid), ("Image clipping", "hidden", clipping), ("Deterministic ties", "hidden", deterministic_ties), ("Descending confidence", "hidden", score_order), ("Inclusive threshold and zero-area policy", "hidden", inclusive_zero_and_empty_area), ("Invalid prediction tensors", "hidden", invalid_prediction), ("Invalid size or threshold", "hidden", invalid_size_threshold), ("Independent output storage", "hidden", immutability)]
