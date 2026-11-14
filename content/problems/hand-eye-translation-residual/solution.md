# Solution

Validate rigid transforms, build a 3N-by-3 system, and solve it by SVD-backed least squares. O(N) time/storage with fixed three unknowns.

```python
import numpy as np

def _real(value):
    try:
        a = np.asarray(value)
        if a.dtype.kind not in "iuf": raise ValueError("Expected real numeric data")
        a = a.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(a).all() or np.any(np.abs(a)>1e9):
        raise ValueError("Values must be finite with magnitude <=1e9")
    return a

def _rotation(value):
    R=_real(value)
    if R.shape!=(3,3) or not np.allclose(R.T@R,np.eye(3),rtol=0,atol=1e-8) or abs(np.linalg.det(R)-1)>1e-8: raise ValueError("Expected proper rotation")
    return R

def _transform(value):
    T=_real(value)
    if T.shape!=(4,4) or not np.allclose(T[3],[0,0,0,1],rtol=0,atol=1e-8): raise ValueError("Expected homogeneous transform")
    _rotation(T[:3,:3]); return T

def solve_hand_eye_translation(A, B, rotation):
    A,B=map(_real,(A,B)); R=_rotation(rotation)
    if A.ndim!=3 or A.shape[1:]!=(4,4) or not 2<=len(A)<=1000 or B.shape!=A.shape: raise ValueError("Invalid motion-pair shape")
    for transform in np.concatenate([A,B]): _transform(transform)
    C=(A[:,:3,:3]-np.eye(3)).reshape(-1,3); d=(B[:,:3,3]@R.T-A[:,:3,3]).reshape(-1)
    t,_,rank,_=np.linalg.lstsq(C,d,rcond=1e-10)
    if rank<3: raise ValueError("Translation is unobservable")
    return t,(C@t-d).reshape(-1,3)
```
