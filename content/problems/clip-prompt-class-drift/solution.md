# Solution

Normalize embeddings/counts, compute per-class cosine distance and two masked KL terms. O(CD) time.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def prompt_class_drift(old_prototypes, new_prototypes, old_counts, new_counts):
    a=_array(old_prototypes,2);b=_array(new_prototypes,2);x=_array(old_counts,1,"i");y=_array(new_counts,1,"i")
    if not (1<=a.shape[0]<=256 and 1<=a.shape[1]<=512) or b.shape!=a.shape or x.shape!=(len(a),) or y.shape!=x.shape or np.any(x<0) or np.any(y<0) or np.any(x>1000000) or np.any(y>1000000) or x.sum()==0 or y.sum()==0:raise ValueError("Drift contract")
    na=np.linalg.norm(a,axis=1);nb=np.linalg.norm(b,axis=1)
    if np.any(na<1e-8) or np.any(nb<1e-8):raise ValueError("Zero prototype")
    distances=np.clip(1-np.sum((a/na[:,None])*(b/nb[:,None]),axis=1),0,2)
    p=x/x.sum();q=y/y.sum();mid=(p+q)/2;js=0.
    for h in (p,q):
        use=h>0;js+=.5*np.sum(h[use]*np.log(h[use]/mid[use]))
    return distances,float(js)
```
