# Solution

Compute integer token/storage counts and sort each supplied latency row. O(RK log K) time.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def profile_vit(resolutions, patch_size, heads, bytes_per_value, latency_ms):
    r=_array(resolutions,2,"i");l=_array(latency_ms,2)
    if r.shape[1:]!=(2,) or len(r)>128 or l.shape[0]!=len(r) or not 1<=l.shape[1]<=4096 or np.any(l<=0):raise ValueError("Profile shapes")
    if type(patch_size) is not int or not 1<=patch_size<=256 or type(heads) is not int or not 1<=heads<=128 or type(bytes_per_value) is not int or bytes_per_value not in (2,4,8):raise ValueError("Configuration")
    if np.any(r<1) or np.any(r>8192) or np.any(r%patch_size):raise ValueError("Patch grid")
    tokens=(r[:,0]//patch_size)*(r[:,1]//patch_size)+1
    memory=[heads*int(n)*int(n)*bytes_per_value for n in tokens]
    if any(n>np.iinfo(np.int64).max for n in memory):raise ValueError("Memory count overflow")
    rank=(95*l.shape[1]+99)//100-1
    return dict(tokens=tokens.astype(np.int64),attention_bytes=np.array(memory,dtype=np.int64),p95_latency_ms=np.sort(l,axis=1)[:,rank].copy())
```
