# Solution

Allocate the target grid and visit objects once, retaining the best candidate per cell. O(N+S²) time/storage.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def assign_yolo_cells(boxes, labels, grid_size, num_classes):
    b=_array(boxes,2);l=_array(labels,1,"i")
    if b.shape[1:]!=(4,) or len(b)>4096 or l.shape!=(len(b),) or type(grid_size) is not int or not 1<=grid_size<=64 or type(num_classes) is not int or not 1<=num_classes<=256:raise ValueError("Target shape/config")
    if np.any(b[:,:2]<0) or np.any(b[:,:2]>=1) or np.any(b[:,2:]<=0) or np.any(b[:,2:]>1) or np.any(l<0) or np.any(l>=num_classes):raise ValueError("Target range")
    s=grid_size;indices=np.full((s,s),-1,dtype=np.int64);classes=indices.copy();targets=np.zeros((s,s,4));areas=np.full((s,s),-1.)
    for i,(cx,cy,w,h) in enumerate(b):
        row,col=int(np.floor(cy*s)),int(np.floor(cx*s));area=w*h
        if area>areas[row,col]:
            areas[row,col]=area;indices[row,col]=i;classes[row,col]=l[i];targets[row,col]=[cx*s-col,cy*s-row,w,h]
    return dict(object_indices=indices,class_ids=classes,box_targets=targets)
```
