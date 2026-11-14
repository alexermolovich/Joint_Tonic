import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def _rotation(r):
    if r.shape[-2:]!=(3,3) or not np.allclose(r.swapaxes(-1,-2)@r,np.eye(3),atol=1e-9,rtol=0) or not np.allclose(np.linalg.det(r),1,atol=1e-9,rtol=0):raise ValueError("proper rotation required")
    return r

def _transform(t):
    if t.shape[-2:]!=(4,4) or not np.allclose(t[...,3,:],[0,0,0,1],atol=1e-9,rtol=0):raise ValueError("rigid transform required")
    _rotation(t[...,:3,:3]);return t

def warp_pixels(pixels,inverse_depth,source_intrinsics,target_intrinsics,target_from_source,target_size):
    uv=_array(pixels,2);rho=_array(inverse_depth,1);src=_array(source_intrinsics,1);dst=_array(target_intrinsics,1);t=_array(target_from_source,2);size=_array(target_size,1,"i")
    if uv.shape[1]!=2 or len(uv)>16384 or rho.shape!=(len(uv),) or np.any(rho<1e-6) or src.shape!=(4,) or dst.shape!=(4,) or np.any(src[:2]<1e-3) or np.any(dst[:2]<1e-3) or t.shape!=(4,4) or size.shape!=(2,) or np.any((size<1)|(size>4096)):raise ValueError("calibrated warp contract")
    _transform(t);p=np.column_stack([(uv-src[2:])/src[:2],np.ones(len(uv))])/rho[:,None];out=p@t[:3,:3].T+t[:3,3];front=out[:,2]>1e-9;projected=np.full((len(uv),2),np.nan)
    projected[front]=(out[front,:2]/out[front,2,None])*dst[:2]+dst[2:]
    visible=front&(projected[:,0]>=0)&(projected[:,0]<size[1])&(projected[:,1]>=0)&(projected[:,1]<size[0])
    return dict(target_points=out,target_pixels=projected,visible=visible)
