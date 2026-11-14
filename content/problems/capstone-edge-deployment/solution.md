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

import hashlib,hmac,json

def edge_deployment(latency, quality, drift, sizes, intervals, model_bytes, preprocessing, fixture_key, min_quality, budget_ms, memory_budget, max_drift, active):
    latency=_array(latency,2);quality=_array(quality,1);drift=_array(drift,1);sizes=_array(sizes,2,"i");intervals=_array(intervals,2,"i")
    M,R=latency.shape
    if sizes.shape[0]!=M:raise ValueError("models")
    K=sizes.shape[1]
    if not(1<=M<=16 and 1<=R<=128 and 1<=K<=64) or quality.shape!=(M,) or drift.shape!=(M,) or intervals.shape!=(K,2):raise ValueError("shapes")
    if np.any((latency<=0)|(latency>10000)) or np.any((quality<0)|(quality>1)) or np.any((drift<0)|(drift>1)) or np.any((sizes<1)|(sizes>1000000)) or np.any(intervals<0) or np.any(intervals>1024) or np.any(intervals[:,0]>=intervals[:,1]):raise ValueError("ranges")
    if type(model_bytes) is not list or len(model_bytes)!=M or any(type(x) is not bytes or not 1<=len(x)<=4096 for x in model_bytes):raise ValueError("model artifacts")
    if type(preprocessing) is not str or preprocessing not in ('rgb-0-1','bgr-mean') or type(fixture_key) is not bytes or len(fixture_key)!=32 or type(active) is not bool:raise ValueError("package contract")
    minq=_scalar(min_quality,0,1);budget=_scalar(budget_ms,0,10000);maxd=_scalar(max_drift,0,1)
    if type(memory_budget) is not int or not 1<=memory_budget<=64000000:raise ValueError("memory")
    ids=np.empty((M,K),np.int64);allocated=np.zeros(M,np.int64)
    order=sorted(range(K),key=lambda i:(int(intervals[i,0]),i))
    for m in range(M):
        capacity=[];ends=[]
        for i in order:
            start,end=map(int,intervals[i]);size=int(sizes[m,i]);available=[j for j in range(len(capacity)) if ends[j]<=start and capacity[j]>=size]
            if available:chosen=min(available,key=lambda j:(capacity[j],j));ends[chosen]=end
            else:chosen=len(capacity);capacity.append(size);ends.append(end)
            ids[m,i]=chosen
        allocated[m]=sum(capacity)
    p95=np.sort(latency,axis=1)[:,int(np.ceil(.95*R))-1].copy();eligible=[i for i in range(M) if quality[i]>=minq and p95[i]<=budget and allocated[i]<=memory_budget]
    chosen=min(eligible,key=lambda i:(-quality[i],p95[i],i)) if eligible else -1
    passed=chosen>=0 and drift[chosen]<=maxd;manifest=digest=signature=None
    if chosen>=0:
        record=dict(allocated_bytes=int(allocated[chosen]),candidate=chosen,model_sha256=hashlib.sha256(model_bytes[chosen]).hexdigest(),preprocessing=preprocessing,schema=1)
        manifest=json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=True);payload=manifest.encode('ascii');digest=hashlib.sha256(payload).hexdigest();signature=hmac.new(fixture_key,payload,hashlib.sha256).hexdigest()
    return dict(candidate=chosen,buffer_ids=ids,allocated_bytes=allocated,p95_ms=p95,decision='promote' if passed else 'rollback' if active else 'hold',manifest=manifest,sha256=digest,signature=signature)
```
