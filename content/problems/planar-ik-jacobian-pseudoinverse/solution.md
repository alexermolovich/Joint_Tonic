# Solution

Each iteration solves a fixed2x2 SVD and bounds the update; O(I) time and error-history memory for I iterations.

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

def solve_planar_ik(lengths, initial_q, target, max_iterations, tolerance, max_step):
    L,q,g,tol,step=map(_real,(lengths,initial_q,target,tolerance,max_step))
    if L.shape!=(2,) or q.shape!=(2,) or g.shape!=(2,) or np.any(L<1e-9) or tol.ndim!=0 or tol<=0 or step.ndim!=0 or step<=0 or isinstance(max_iterations,(bool,np.bool_)) or not isinstance(max_iterations,(int,np.integer)) or not 0<=max_iterations<=200: raise ValueError("Invalid IK contract")
    q=q.copy(); errors=[]
    for iteration in range(max_iterations+1):
        a,b=q[0],q.sum(); c1,s1,c2,s2=np.cos(a),np.sin(a),np.cos(b),np.sin(b)
        position=np.array([L[0]*c1+L[1]*c2,L[0]*s1+L[1]*s2]); error=g-position; norm=float(np.linalg.norm(error)); errors.append(norm)
        if norm<=tol or iteration==max_iterations: return q,bool(norm<=tol),np.asarray(errors,dtype=np.float64)
        J=np.array([[-L[0]*s1-L[1]*s2,-L[1]*s2],[L[0]*c1+L[1]*c2,L[1]*c2]])
        dq=np.linalg.pinv(J,rcond=1e-12)@error; length=np.linalg.norm(dq)
        if length>step: dq=dq*(step/length)
        q=q+dq
```
