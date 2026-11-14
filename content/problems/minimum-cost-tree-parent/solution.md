# Solution

O(N) time and memory. Add root and edge costs, replace infeasible totals by infinity, and select the first minimum only when a feasible candidate exists.

```python
import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int, float) or not low <= x <= high or not np.isfinite(x):
        raise ValueError("Scalar outside contract")
    return float(x)

def choose_tree_parent(root_costs,edge_costs,feasible):
    root=_array(root_costs,1);edge=_array(edge_costs,1);valid=_array(feasible,1,"b")
    if not 0<=len(root)<=100000 or edge.shape!=root.shape or valid.shape!=root.shape or np.any(root<0) or np.any(edge<0):raise ValueError("parent cost contract")
    if not valid.any():return dict(parent=-1,total_cost=float('inf'))
    total=np.where(valid,root+edge,np.inf);i=int(np.argmin(total));return dict(parent=i,total_cost=float(total[i]))
```
