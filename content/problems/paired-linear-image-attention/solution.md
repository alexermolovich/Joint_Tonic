# Solution

Compute masked key/value summaries for each self and cross message. Save both self outputs before either cross update. Runtime O((N+M)D^2), avoiding materializing NM similarities; working storage O((N+M)D+D^2).

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x,low,high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def paired_attention(source,target,weights,source_valid,target_valid):
    a=_array(source,2);b=_array(target,2);w=_array(weights,3);ma=_array(source_valid,1,"b");mb=_array(target_valid,1,"b");d=a.shape[1]
    if not 1<=d<=32 or b.shape[1]!=d or len(a)>256 or len(b)>256 or w.shape!=(4,d,d) or ma.shape!=(len(a),) or mb.shape!=(len(b),) or np.any(np.abs(a)>10) or np.any(np.abs(b)>10) or np.any(np.abs(w)>2):raise ValueError("paired attention contract")
    def message(x,y,mx,my):
        q=x@w[0];k=y@w[1];q=np.where(q>=0,q+1,np.exp(np.minimum(q,0)));k=np.where(k>=0,k+1,np.exp(np.minimum(k,0)));k=np.where(my[:,None],k,0);v=np.where(my[:,None],y@w[2],0)
        numerator=q@(k.T@v);denominator=np.maximum(q@k.sum(axis=0),1e-9);out=(numerator/denominator[:,None])@w[3]
        return np.where(mx[:,None],out,0)
    a0=np.where(ma[:,None],a,0);b0=np.where(mb[:,None],b,0);a1=a0+message(a0,a0,ma,ma);b1=b0+message(b0,b0,mb,mb)
    return dict(self_source=a1,self_target=b1,source=a1+message(a1,b1,ma,mb),target=b1+message(b1,a1,mb,ma))
```
