# Reference solution

Validate the common grid; use the validity mask before reshaping both arrays. Broadcast positions across batches, build row/column coordinates, and copy outputs so they share no storage with inputs or one another.

A detector can attend to the wrong location if position vectors use column-major order while features use row-major order. Padded regions must stay masked even when their zero features resemble a real dark region.

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

def flatten_spatial(features, positions, valid):
    array(features,4);array(positions,3);array(valid,3,np.bool_)
    b,h,w,d=features.shape
    check(1<=b<=16 and 1<=h<=32 and 1<=w<=32 and 1<=d<=32 and positions.shape==(h,w,d) and valid.shape==(b,h,w))
    tokens=np.where(valid[...,None],features,0).reshape(b,h*w,d).copy()
    pos=np.where(valid[...,None],positions[None],0).reshape(b,h*w,d).copy()
    coordinates=np.stack(np.indices((h,w)),axis=-1).reshape(h*w,2).astype(np.int64)
    return dict(tokens=tokens,position_tokens=pos,padding=(~valid).reshape(b,h*w).copy(),coordinates=coordinates)
```
