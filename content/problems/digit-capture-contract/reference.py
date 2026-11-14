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

def capture_health(frames,timestamps,frame_ids,exposure_us,expected_exposure_us,max_gap):
    if not isinstance(frames,np.ndarray) or frames.dtype!=np.uint8 or frames.ndim!=4:raise ValueError("uint8 capture required")
    n,h,w,c=frames.shape;t=_array(timestamps,1);ids=_array(frame_ids,1,"int");e=_array(exposure_us,1);expected=_scalar(expected_exposure_us,1,1e6);gap=_scalar(max_gap,1e-6,100)
    if n>64 or not 1<=h<=64 or not 1<=w<=64 or c!=3 or any(x.shape!=(n,) for x in [t,ids,e]) or (t<0).any() or (ids<0).any() or (e<1).any():raise ValueError("capture metadata contract")
    flags=np.zeros((n,4),bool);flags[1:,0]=(np.diff(t)<=0)|(np.diff(t)>gap);flags[1:,1]=np.diff(ids)!=1;flags[:,2]=np.abs(e-expected)>.05*expected
    fraction=np.mean((frames==0)|(frames==255),axis=(1,2,3));flags[:,3]=fraction>.95;usable=~flags.any(axis=1)
    return {'flags':flags,'usable':usable,'saturation_fraction':fraction,'ready':bool(n and usable.all())}
