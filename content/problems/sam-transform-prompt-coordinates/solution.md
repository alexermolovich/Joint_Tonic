# Reference solution

Compute rounded image dimensions, reject a collapsed axis, multiply x and y by their own realized ratios and return a fresh point array.

A segmentation prompt can miss a small grasp target if it is scaled with the unrounded image height. Confusing `(x,y)` with `(height,width)` is another common integration failure. These coordinates still require calibration before robot-frame use.

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

def resize_prompt_coordinates(points, image_height, image_width, target_length):
    array(points,2);integer(image_height,1,8192);integer(image_width,1,8192);integer(target_length,1,2048)
    check(points.shape[1]==2 and points.shape[0]<=4096)
    check(np.all(points>=0) and np.all(points<=np.array([image_width,image_height])))
    scale=target_length/max(image_height,image_width)
    h=math.floor(image_height*scale+.5);w=math.floor(image_width*scale+.5)
    check(h>0 and w>0)
    return dict(points=points*np.array([w/image_width,h/image_height]),resized_shape=np.array([h,w],dtype=np.int64))
```
