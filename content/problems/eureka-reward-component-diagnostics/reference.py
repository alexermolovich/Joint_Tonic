import numpy as np

def _array(value, ndim=None, kind="real"):
    try: a=np.asarray(value)
    except (ValueError,TypeError,OverflowError) as e: raise ValueError("invalid array") from e
    if ndim is not None and a.ndim!=ndim: raise ValueError("invalid rank")
    if a.size>1000000: raise ValueError("array too large")
    if kind=="bool":
        if a.dtype.kind!='b': raise ValueError("boolean array required")
        return a.copy()
    if kind=="int":
        if a.dtype.kind not in 'iu': raise ValueError("integer array required")
    elif a.dtype.kind not in 'iuf': raise ValueError("real numeric array required")
    if not np.isfinite(a).all() or (np.abs(a.astype(np.float64))>1e6).any(): raise ValueError("invalid numeric values")
    return a.astype(np.int64 if kind=="int" else np.float64)

def _scalar(x,low=0,high=1e6,integer=False):
    if isinstance(x,(bool,np.bool_)) or not isinstance(x,(int,float,np.integer,np.floating)): raise ValueError("numeric scalar required")
    if integer and not isinstance(x,(int,np.integer)): raise ValueError("integer scalar required")
    if not low<=x<=high or not np.isfinite(x): raise ValueError("scalar outside bounds")
    return int(x) if integer else float(x)

def reward_diagnostics(components,task_scores,valid):
    x=_array(components,3);y=_array(task_scores,2);m=_array(valid,2,"bool");b,t,c=x.shape
    if not 1<=b<=64 or not 1<=t<=1024 or not 1<=c<=16 or y.shape!=(b,t) or m.shape!=(b,t):raise ValueError("diagnostic shape")
    a=x[m];score=y[m];n=len(a);out={k:np.full(c,np.nan) for k in ['mean','std','mean_abs','correlation']}
    if n:
        mean=a.mean(axis=0);center=a-mean;scale=np.max(np.abs(center),axis=0);normalized=np.divide(center,scale,out=np.zeros_like(center),where=scale>0);sd=np.sqrt(np.mean(normalized*normalized,axis=0));yc=score-score.mean();yscale=np.max(np.abs(yc));yn=yc/yscale if yscale>0 else np.zeros_like(yc);ysd=np.sqrt(np.mean(yn*yn));den=sd*ysd;corr=np.divide(np.mean(normalized*yn[:,None],axis=0),den,out=np.full(c,np.nan),where=den>0)
        out={'mean':mean,'std':scale*sd,'mean_abs':np.abs(a).mean(axis=0),'correlation':corr}
    return {'count':n,**out}
