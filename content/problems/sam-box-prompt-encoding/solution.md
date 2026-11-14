# Solution

Vectorize the same Fourier map over box and corner axes, then add distinct corner vectors. O(NF) time/storage.

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

def encode_boxes(boxes, image_size, frequencies, corner_embeddings):
    b=_array(boxes,2);f,e=_prompt_parameters(image_size,frequencies,corner_embeddings);h,w=image_size
    if b.shape[1:]!=(4,) or len(b)>2048 or np.any(b<0) or np.any(b[:,0]>b[:,2]) or np.any(b[:,1]>b[:,3]) or np.any(b[:,[0,2]]>w-1) or np.any(b[:,[1,3]]>h-1):raise ValueError("Box contract")
    p=b.reshape(-1,2,2)
    phase=(2*(p+.5)/np.array([w,h])-1)@f*(2*np.pi)
    return np.concatenate((np.sin(phase),np.cos(phase)),axis=2)+e[None]
```
