# Solution

Convert keypoints to descriptor coordinates, sample four channel vectors, and normalize only nonzero interpolants. O(ND) time and output memory. Keep geometric support separate from descriptor magnitude.

```python
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

def _sample(image,points):
    h,w=image.shape[:2];inside=(points[:,0]>=0)&(points[:,0]<=w-1)&(points[:,1]>=0)&(points[:,1]<=h-1);out=np.zeros((len(points),)+image.shape[2:])
    xy=points[inside];lo=np.floor(xy).astype(np.int64);hi=np.minimum(lo+1,[w-1,h-1]);f=xy-lo
    for i,j in ((0,0),(1,0),(0,1),(1,1)):
        x=hi[:,0] if i else lo[:,0];y=hi[:,1] if j else lo[:,1];weight=(f[:,0] if i else 1-f[:,0])*(f[:,1] if j else 1-f[:,1])
        out[inside]+=image[y,x]*weight.reshape((-1,)+(1,)*(image.ndim-2))
    return out,inside

def sample_descriptors(descriptor_map,keypoints,stride,offset):
    image=_array(descriptor_map,3);p=_array(keypoints,2);s=_array(stride,1);o=_array(offset,1);h,w,d=image.shape
    if not all(1<=v<=128 for v in image.shape) or image.size>1000000 or np.any(np.abs(image)>100) or p.shape[1]!=2 or len(p)>4096 or len(p)*d>524288 or s.shape!=(2,) or o.shape!=(2,) or np.any((s<1e-3)|(s>64)):raise ValueError("descriptor sampling contract")
    samples,valid=_sample(image,(p-o)/s);norm=np.linalg.norm(samples,axis=1);out=np.divide(samples,norm[:,None],out=np.zeros_like(samples),where=norm[:,None]>1e-12)
    return dict(descriptors=out,valid=valid)
```
