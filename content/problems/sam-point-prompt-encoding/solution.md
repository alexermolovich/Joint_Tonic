# Solution

Form centered normalized coordinates, project frequencies and concatenate sine/cosine channels, then add type embeddings. O(NF) time/storage.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _prompt_parameters(size, frequencies, embeddings):
    f=_array(frequencies,2);e=_array(embeddings,2)
    if type(size) is not tuple or len(size)!=2 or any(type(v) is not int or not 1<=v<=100000 for v in size):raise ValueError("Image size")
    if f.shape[0]!=2 or not 1<=f.shape[1]<=128 or e.shape!=(2,2*f.shape[1]) or np.any(np.abs(f)>100):raise ValueError("Embedding shape")
    return f,e

def encode_points(points, labels, image_size, frequencies, type_embeddings):
    p=_array(points,2);l=_array(labels,1,"i");f,e=_prompt_parameters(image_size,frequencies,type_embeddings)
    h,w=image_size
    if p.shape[1:]!=(2,) or len(p)>4096 or l.shape!=(len(p),) or np.any((l<0)|(l>1)) or np.any(p<0) or np.any(p[:,0]>w-1) or np.any(p[:,1]>h-1):raise ValueError("Point contract")
    phase=(2*(p+.5)/np.array([w,h])-1)@f*(2*np.pi)
    return np.concatenate((np.sin(phase),np.cos(phase)),axis=1)+e[l]
```
