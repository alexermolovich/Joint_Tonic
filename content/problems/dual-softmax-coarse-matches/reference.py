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

def coarse_matches(source,target,source_valid,target_valid,temperature,threshold):
    a=_array(source,2);b=_array(target,2);ma=_array(source_valid,1,"b");mb=_array(target_valid,1,"b");tau=_scalar(temperature,1e-3,100);limit=_scalar(threshold,0,1);n,d=a.shape;m=len(b)
    if not 1<=d<=128 or b.shape[1]!=d or n>512 or m>512 or ma.shape!=(n,) or mb.shape!=(m,) or np.any(np.abs(a)>100) or np.any(np.abs(b)>100):raise ValueError("coarse matching contract")
    confidence=np.zeros((n,m));pairs=np.empty((0,2),np.int64);values=np.empty(0)
    ia=np.flatnonzero(ma);ib=np.flatnonzero(mb)
    if len(ia) and len(ib):
        s=(a[ia]@b[ib].T)/(d*tau);row=np.exp(s-s.max(axis=1,keepdims=True));row/=row.sum(axis=1,keepdims=True);column=np.exp(s-s.max(axis=0,keepdims=True));column/=column.sum(axis=0,keepdims=True);p=row*column;confidence[np.ix_(ia,ib)]=p
        j=np.argmax(p,axis=1);i=np.argmax(p,axis=0);rows=np.arange(len(ia));keep=(i[j]==rows)&(p[rows,j]>limit);pairs=np.column_stack([ia[keep],ib[j[keep]]]);values=p[rows[keep],j[keep]].copy()
    return dict(confidence=confidence,pairs=pairs,match_confidence=values)
