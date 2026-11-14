from numbers import Real
import numpy as np


def _record(record):
    if not isinstance(record, dict) or not {"matrix", "target", "source", "stamp", "unit"} <= record.keys():
        raise ValueError("Expected a complete transform record")
    for field in ("target", "source"):
        if not isinstance(record[field], str) or not record[field] or record[field].strip() != record[field]:
            raise ValueError("Frame names must be nonempty strings without surrounding whitespace")
    stamp = record["stamp"]
    if not isinstance(stamp, Real) or isinstance(stamp, bool) or not -1e6 <= stamp <= 1e6:
        raise ValueError("Invalid measurement timestamp")
    if not isinstance(record["unit"], str) or record["unit"] != "m":
        raise ValueError("Translations must use meters")


def _matrix(value):
    try:
        raw = np.asarray(value)
        if raw.dtype.kind not in "iuf":
            raise ValueError("Expected real numeric matrix")
        T = raw.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Invalid matrix") from exc
    if T.shape != (4, 4) or not np.isfinite(T).all():
        raise ValueError("Expected finite (4,4) matrix")
    R = T[:3, :3]
    if np.any(np.abs(T[:3, 3]) > 1e6) or np.any(np.abs(R) > 1 + 1e-9):
        raise ValueError("Invalid rotation or translation magnitude")
    if not np.allclose(T[3], [0, 0, 0, 1], atol=1e-9, rtol=0):
        raise ValueError("Invalid homogeneous bottom row")
    if not np.allclose(R.T @ R, np.eye(3), atol=1e-9, rtol=0) or not np.isclose(np.linalg.det(R), 1, atol=1e-9, rtol=0):
        raise ValueError("Rotation must be proper and orthonormal")
    return T


def compose_transforms(first, second):
    _record(first); _record(second)
    if first["source"] != second["target"] or first["stamp"] != second["stamp"]:
        raise ValueError("Incompatible middle frame or timestamp")
    a, b = _matrix(first["matrix"]), _matrix(second["matrix"])
    forward = np.eye(4)
    forward[:3, :3] = a[:3, :3] @ b[:3, :3]
    forward[:3, 3] = a[:3, :3] @ b[:3, 3] + a[:3, 3]
    inverse = np.eye(4)
    inverse[:3, :3] = forward[:3, :3].T
    inverse[:3, 3] = -inverse[:3, :3] @ forward[:3, 3]
    return forward, inverse
