# Reference solution

Build the in-bounds mask, replace unused coordinates before indexing, gather four camera-specific neighbors and blend with fractional offsets. Zero all unused output vectors.

BEV perception combines evidence from calibrated cameras. Using original image coordinates directly on a downsampled feature map selects the wrong evidence. An out-of-view point must not be clipped into a plausible border observation.

```python
import numpy as np
import math

def array(x, ndim, dtype=np.float64):
    if not isinstance(x,np.ndarray) or x.dtype != np.dtype(dtype) or x.ndim != ndim or x.size>2000000:
        raise ValueError("Invalid array type, dtype, rank or size")
    if dtype != np.bool_ and (not np.isfinite(x).all() or np.any(np.abs(x.astype(float))>1e6)):
        raise ValueError("Nonfinite or out-of-range data")
    return x

def check(ok):
    if not ok: raise ValueError("Contract violation")

def real(x, low, high):
    check(type(x) in (int,float) and math.isfinite(x) and low<=x<=high)
    return x

def integer(x, low, high):
    check(type(x) is int and low<=x<=high)
    return x

def sample_camera_features(features, coordinates, valid):
    array(features,4);array(coordinates,3);array(valid,2,np.bool_)
    c,h,w,d=features.shape
    check(1<=c<=8 and 1<=h<=64 and 1<=w<=64 and 1<=d<=32 and coordinates.shape[0]==c and coordinates.shape[2]==2)
    n=coordinates.shape[1];check(n<=4096 and valid.shape==(c,n))
    u=coordinates[...,0];v=coordinates[...,1];used=valid&(u>=0)&(u<=w-1)&(v>=0)&(v<=h-1)
    # Replace unused coordinates before integer indexing, including out-of-bounds values.
    u=np.where(used,u,0);v=np.where(used,v,0)
    x=np.floor(u).astype(int);y=np.floor(v).astype(int);xx=np.minimum(x+1,w-1);yy=np.minimum(y+1,h-1)
    dx=(u-x)[...,None];dy=(v-y)[...,None];camera=np.arange(c)[:,None]
    samples=(1-dy)*((1-dx)*features[camera,y,x]+dx*features[camera,y,xx])+dy*((1-dx)*features[camera,yy,x]+dx*features[camera,yy,xx])
    return dict(samples=np.where(used[...,None],samples,0),used=used)
```
