import numpy as np


def _unit(value):
    try:
        raw=np.asarray(value)
        if raw.dtype.kind not in "iuf":
            raise ValueError("Expected real quaternion")
        q=raw.astype(np.float64)
    except (TypeError,OverflowError) as exc:
        raise ValueError("Expected real quaternion") from exc
    if q.shape!=(4,) or not np.isfinite(q).all() or np.any(np.abs(q)>1e6):
        raise ValueError("Quaternion must be finite (4,) and bounded")
    scale=np.max(np.abs(q))
    if scale==0:
        raise ValueError("Zero quaternion has no orientation")
    scaled=q/scale
    return scaled/np.linalg.norm(scaled)


def compose_quaternions(q_after,q_before):
    a,b=_unit(q_after),_unit(q_before)
    result=np.empty(4,dtype=np.float64)
    result[0]=a[0]*b[0]-np.dot(a[1:],b[1:])
    result[1:]=a[0]*b[1:]+b[0]*a[1:]+np.cross(a[1:],b[1:])
    return result/np.linalg.norm(result)
