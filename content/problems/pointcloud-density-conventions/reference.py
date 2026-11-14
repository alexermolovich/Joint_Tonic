import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def audit_cloud(points, unit, frame, expected_frame, voxel_size):
    import re
    p=_array(points,2)
    if p.shape[1:]!=(3,) or len(p)>4096 or type(unit) is not str or unit not in ('m','cm','mm'):raise ValueError("Cloud or unit")
    if any(type(v) is not str or re.fullmatch('[A-Za-z0-9_]{1,32}',v) is None for v in (frame,expected_frame)):raise ValueError("Frame labels")
    if type(voxel_size) not in (int,float) or not 1e-4<=voxel_size<=1000:raise ValueError("Voxel size")
    x=p*{'m':1.,'cm':.01,'mm':.001}[unit]
    count=len(np.unique(np.floor(x/voxel_size).astype(np.int64),axis=0))
    return dict(frame_matches=frame==expected_frame,occupied_voxels=count,points_per_voxel=float(len(p)/count) if count else 0.,extent_m=np.ptp(x,axis=0) if len(p) else np.zeros(3))
