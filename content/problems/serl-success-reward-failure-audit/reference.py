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

def audit_success_rewards(probabilities,success,failure_type,valid,threshold,num_failure_types):
    p=_array(probabilities,1);y=_array(success,1,"bool");types=_array(failure_type,1,"int");m=_array(valid,1,"bool");tau=_scalar(threshold,0,1)
    if type(num_failure_types) is not int:raise ValueError("failure category count")
    k=_scalar(num_failure_types,1,32,True)
    if len(p)>16384 or y.shape!=p.shape or types.shape!=p.shape or m.shape!=p.shape or ((p<0)|(p>1)).any() or (types[y]!=-1).any() or ((types[~y]<0)|(types[~y]>=k)).any():raise ValueError("classifier audit contract")
    predicted=p>=tau;tp=int((m&y&predicted).sum());fp=int((m&~y&predicted).sum());fn=int((m&y&~predicted).sum());tn=int((m&~y&~predicted).sum());failed=m&~y;counts=np.bincount(types[failed],minlength=k).astype(np.int64);false=np.bincount(types[failed&predicted],minlength=k).astype(np.int64);rate=np.divide(false,counts,out=np.full(k,np.nan),where=counts>0)
    return {'confusion':np.array([tp,fp,fn,tn],np.int64),'precision':tp/(tp+fp) if tp+fp else float('nan'),'recall':tp/(tp+fn) if tp+fn else float('nan'),'failure_counts':counts,'false_positive_counts':false,'false_positive_rate':rate}
