# Reference solution

Validate all digest strings and the exact shape tuple; serialize the fixed record canonically, hash its ASCII bytes, then compare to the optional cached key.

Reusing a SAM embedding after changing normalization can silently misalign prompt results. Image-only cache keys miss this dependency. A storage layer must separately verify the embedding's own checksum and access policy.

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

def embedding_cache_key(image_sha256, encoder_sha256, preprocessing_sha256, resized_shape, cached_key):
    import hashlib,json,re
    def digest(x):return isinstance(x,str) and re.fullmatch('[0-9a-f]{64}',x) is not None
    check(all(digest(x) for x in (image_sha256,encoder_sha256,preprocessing_sha256)))
    check(type(resized_shape) is tuple and len(resized_shape)==2)
    for x in resized_shape:integer(x,1,8192)
    check(cached_key is None or digest(cached_key))
    record=dict(schema=1,image_sha256=image_sha256,encoder_sha256=encoder_sha256,preprocessing_sha256=preprocessing_sha256,resized_shape=list(resized_shape))
    key=hashlib.sha256(json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode('ascii')).hexdigest()
    return dict(key=key,hit=cached_key==key)
```
