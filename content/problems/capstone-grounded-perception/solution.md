# Solution

Follow the stage equations in Theory. The reference composes bounded NumPy operations and explicit validation; it never executes a trained model or contacts a robot. Runtime is linear in supplied tensor entries except the documented buffer allocation search.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int, float) or not low <= x <= high or not np.isfinite(x):
        raise ValueError("Invalid scalar")
    return float(x)

def grounded_perception(masks, depth, scores, latency, K, world_from_camera, previous, min_score, budget_ms, max_invalid, active):
    masks=_array(masks,3,"b");depth=_array(depth,2);scores=_array(scores,1);latency=_array(latency,1)
    K=_array(K,2);T=_array(world_from_camera,2);previous=_array(previous,2)
    n,h,w=masks.shape
    if not (1<=n<=64 and 1<=h<=64 and 1<=w<=64) or depth.shape!=(h,w) or scores.shape!=(n,) or latency.shape!=(n,):raise ValueError("shapes")
    if np.any((depth<0)|(depth>100)) or np.any((scores<0)|(scores>1)) or np.any((latency<0)|(latency>10000)):raise ValueError("ranges")
    if K.shape!=(3,3) or K[0,1]!=0 or K[1,0]!=0 or not np.array_equal(K[2],[0,0,1]) or not (1e-3<=K[0,0]<=1e4 and 1e-3<=K[1,1]<=1e4):raise ValueError("calibration")
    if T.shape!=(4,4) or not np.array_equal(T[3],[0,0,0,1]) or not np.allclose(T[:3,:3].T@T[:3,:3],np.eye(3),atol=1e-9,rtol=0) or abs(np.linalg.det(T[:3,:3])-1)>1e-9:raise ValueError("transform")
    if previous.shape!=(4,4) or np.any(previous<0) or type(active) is not bool:raise ValueError("history/active")
    threshold=_scalar(min_score,0,1);budget=_scalar(budget_ms,0,10000);limit=_scalar(max_invalid,0,1)
    centers=np.full((n,3),np.nan);valid=np.zeros(n,dtype=bool);counts=np.zeros((4,4));eligible=scores>=threshold
    for i in range(n):
        if not eligible[i]:continue
        row,col=np.nonzero(masks[i]&(depth>0))
        if len(row)==0:continue
        z=depth[row,col];p=np.stack(((col-K[0,2])*z/K[0,0],(row-K[1,2])*z/K[1,1],z),axis=1)
        center=(p@T[:3,:3].T+T[:3,3]).mean(axis=0)
        c,r=np.floor(center[:2]+2).astype(np.int64)
        if not (0<=c<4 and 0<=r<4):continue
        centers[i]=center;valid[i]=True;counts[r,c]+=1
    p95=float(np.sort(latency)[int(np.ceil(.95*n))-1]);invalid=float(int(eligible.sum())-int(valid.sum()))/int(eligible.sum()) if eligible.any() else 1.
    passed=valid.any() and invalid<=limit and p95<=budget
    return dict(centroids=centers,valid=valid,bev=.5*previous+.5*counts,p95_ms=p95,invalid_fraction=invalid,decision="promote" if passed else "rollback" if active else "hold")
```
