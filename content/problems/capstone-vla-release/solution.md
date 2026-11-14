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

import hashlib

def vla_release(observations, targets, valid, train, embodiment, tasks, lower, upper, base, projection, adapter, learning_rate, latency, max_mse, budget_ms):
    x=_array(observations,3);y=_array(targets,3);valid=_array(valid,2,"b");train=_array(train,2,"b");emb=_array(embodiment,1,"i");tasks=_array(tasks,1,"i")
    lo=_array(lower,2);hi=_array(upper,2);w=_array(base,2);p=_array(projection,2);b=_array(adapter,2);latency=_array(latency,2)
    B,T,D=x.shape
    if y.shape[:2]!=(B,T):raise ValueError("targets")
    A=y.shape[2];E=lo.shape[0];R=p.shape[1]
    if not (1<=B<=32 and 1<=T<=32 and 1<=D<=16 and 1<=A<=16 and 1<=E<=8 and 1<=R<=D):raise ValueError("sizes")
    if valid.shape!=(B,T) or train.shape!=(B,T) or latency.shape!=(B,T) or emb.shape!=(B,) or tasks.shape!=(B,) or lo.shape!=(E,A) or hi.shape!=(E,A) or w.shape!=(D,A) or p.shape!=(D,R) or b.shape!=(R,A):raise ValueError("shapes")
    if np.any((emb<0)|(emb>=E)) or np.any((tasks<0)|(tasks>=3)) or np.any(train&~valid) or not train.any() or not (valid&~train).any():raise ValueError("identities/masks")
    if np.any(hi-lo<1e-6) or np.any(np.abs(lo)>100) or np.any(np.abs(hi)>100) or any(np.any(np.abs(z)>10) for z in (x,w,p,b)) or np.any((latency<0)|(latency>10000)):raise ValueError("ranges")
    low=lo[emb,None,:];span=hi[emb,None,:]-low
    if np.any(((y<low)|(y>low+span))&valid[:,:,None]):raise ValueError("action bounds")
    lr=_scalar(learning_rate,0,1);mse_limit=_scalar(max_mse,0,40000);budget=_scalar(budget_ms,0,10000)
    xt=x[train];target=(2*(y-low)/span-1)[train];features=xt@p
    updated=b-lr*(2/(len(xt)*A))*(features.T@(xt@w+features@b-target))
    raw=x@w+(x@p)@updated;tokens=np.minimum(15,np.floor(8*(np.clip(raw,-1,1)+1))).astype(np.int64)
    actions=low+((-1+(tokens+.5)/8)+1)*span/2
    tokens=np.where(valid[:,:,None],tokens,-1);actions=np.where(valid[:,:,None],actions,0.)
    held=valid&~train;errors=np.mean((actions-y)**2,axis=2);em=np.full(E,np.nan);tm=np.full(3,np.nan)
    for i in range(E):
        mask=held&(emb[:,None]==i)
        if mask.any():em[i]=errors[mask].mean()
    for i in range(3):
        mask=held&(tasks[:,None]==i)
        if mask.any():tm[i]=errors[mask].mean()
    invalid=float(np.any(np.abs(raw)>1,axis=2)[held].mean());durations=np.sort(latency[held]);p95=float(durations[int(np.ceil(.95*len(durations)))-1])
    passed=invalid==0 and np.nanmax(em)<=mse_limit and np.nanmax(tm)<=mse_limit and p95<=budget
    return dict(adapter=updated,tokens=tokens,actions=actions,embodiment_mse=em,task_mse=tm,invalid_rate=invalid,p95_ms=p95,decision="promote" if passed else "hold",adapter_sha256=hashlib.sha256(updated.astype('<f8').tobytes(order='C')).hexdigest())
```
