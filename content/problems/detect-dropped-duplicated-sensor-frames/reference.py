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

def audit_frame_ids(frame_ids):
    ids=_real(frame_ids)
    if ids.ndim!=1 or np.any(ids<0) or np.any(ids>100000) or np.any(ids!=np.floor(ids)) or np.any(np.diff(ids)<0): raise ValueError("Invalid counters")
    values,counts=np.unique(ids.astype(np.int64),return_counts=True)
    missing=np.setdiff1d(np.arange(values[0],values[-1]+1,dtype=np.int64),values) if len(values) else np.empty(0,dtype=np.int64)
    return {"missing":missing,"duplicates":values[counts>1].copy()}
