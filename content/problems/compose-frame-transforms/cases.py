import copy
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def rec(matrix, target="world", source="base"):
    return dict(matrix=matrix, target=target, source=source, stamp=2., unit="m")


def pair():
    return rec(np.eye(4)), rec(np.eye(4), "base", "camera")


def rotated_mount(m):
    a, b = pair()
    a["matrix"] = np.array([[0, -1, 0, 1], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    b["matrix"][0, 3] = 1
    out, inv = m.compose_transforms(a, b)
    assert_allclose(out, [[0,-1,0,1],[1,0,0,1],[0,0,1,0],[0,0,0,1]], atol=1e-9)
    assert_allclose(inv, [[0,1,0,-1],[-1,0,0,1],[0,0,1,0],[0,0,0,1]], atol=1e-9)


def translations(m):
    a, b = pair(); a["matrix"][0, 3] = 2; b["matrix"][1, 3] = 3
    out, inv = m.compose_transforms(a, b)
    assert_allclose(out[:3, 3], [2, 3, 0]); assert_allclose(inv[:3, 3], [-2, -3, 0])


def labels_and_time(m):
    for field, value in [("target", "wrong"), ("unit", "mm"), ("stamp", 2.000000001),
                         ("source", ""), ("source", " camera"), ("target", 3),
                         ("stamp", True), ("stamp", np.nan), ("stamp", 10**1000)]:
        a, b = pair(); b[field] = value
        with np.testing.assert_raises(ValueError): m.compose_transforms(a, b)
    for value in [None, [], {}, {"matrix":np.eye(4)}]:
        with np.testing.assert_raises(ValueError): m.compose_transforms(value, pair()[1])


def invalid_matrices(m):
    variants = [np.eye(3), np.eye(4).astype(str), np.eye(4).astype(complex), np.eye(4).astype(bool)]
    for position, value in [((0,0),-1),((0,0),2),((0,1),.1),((3,0),.1),((3,3),2),((0,3),np.inf),((0,3),1000001)]:
        matrix = np.eye(4); matrix[position] = value; variants.append(matrix)
    for matrix in variants:
        a, b = pair(); b["matrix"] = matrix
        with np.testing.assert_raises(ValueError): m.compose_transforms(a, b)


def tolerances_and_loop(m):
    a, b = pair()
    b["source"] = "world"; b["extra"] = "ignored"
    b["matrix"][3, 0] = 5e-10
    out, inv = m.compose_transforms(a, b)
    assert_array_equal(out[3], [0,0,0,1]); assert_array_equal(inv[3], [0,0,0,1])
    assert out.dtype == inv.dtype == np.float64


def round_trips(m):
    rng = np.random.default_rng(20261113)
    for _ in range(50):
        a, b = pair()
        for record in (a,b):
            R, _ = np.linalg.qr(rng.normal(size=(3,3)))
            if np.linalg.det(R) < 0: R[:,0] *= -1
            record["matrix"][:3,:3] = R
            record["matrix"][:3,3] = rng.normal(size=3)
        before = copy.deepcopy((a,b))
        out, inv = m.compose_transforms(a,b)
        points = np.column_stack([rng.normal(size=(20,3)), np.ones(20)]).T
        sequential = a["matrix"] @ (b["matrix"] @ points)
        assert_allclose(out @ points, sequential, atol=1e-9)
        assert_allclose(inv @ (out @ points), points, atol=1e-9)
        for original, snapshot in zip((a,b),before):
            assert_array_equal(original["matrix"],snapshot["matrix"])
            assert not np.shares_memory(out,original["matrix"])
            assert not np.shares_memory(inv,original["matrix"])
        assert not np.shares_memory(out,inv)


TESTS=[("Rotated mounting offset","public",rotated_mount),("Two translations","public",translations),
       ("Frame, unit and time contracts","hidden",labels_and_time),("Reject non-rigid matrices","hidden",invalid_matrices),
       ("Tolerances and returning frame","hidden",tolerances_and_loop),("Independent point round trips","hidden",round_trips)]
