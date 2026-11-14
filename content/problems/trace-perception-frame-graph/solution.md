# Solution

Validate the forest with parent-chain cycle checks, then traverse the unique path. At most128edges; O(E²) worst-case validation, O(E) traversal and memory.

```python
import numpy as np

def _real(value):
    try:
        a = np.asarray(value)
        if a.dtype.kind not in "iuf": raise ValueError("Expected real numeric data")
        a = a.astype(np.float64)
    except (TypeError, OverflowError) as exc:
        raise ValueError("Expected real numeric data") from exc
    if not np.isfinite(a).all() or np.any(np.abs(a)>1e9):
        raise ValueError("Values must be finite with magnitude <=1e9")
    return a

def _rotation(value):
    R=_real(value)
    if R.shape!=(3,3) or not np.allclose(R.T@R,np.eye(3),rtol=0,atol=1e-8) or abs(np.linalg.det(R)-1)>1e-8: raise ValueError("Expected proper rotation")
    return R

def _transform(value):
    T=_real(value)
    if T.shape!=(4,4) or not np.allclose(T[3],[0,0,0,1],rtol=0,atol=1e-8): raise ValueError("Expected homogeneous transform")
    _rotation(T[:3,:3]); return T

def resolve_frame_transform(edges, source, target):
    import re
    valid=lambda name:isinstance(name,str) and re.fullmatch(r"[a-z][a-z0-9_]{0,31}",name) is not None
    if not isinstance(edges,list) or len(edges)>128 or not valid(source) or not valid(target): raise ValueError("Invalid frame graph")
    parents={}; graph={}
    for edge in edges:
        if not isinstance(edge,tuple) or len(edge)!=3: raise ValueError("Invalid edge")
        parent,child,value=edge
        if not valid(parent) or not valid(child) or parent==child or child in parents: raise ValueError("Invalid parent relation")
        T=_transform(value); parents[child]=parent
        inverse=np.eye(4); inverse[:3,:3]=T[:3,:3].T; inverse[:3,3]=-T[:3,:3].T@T[:3,3]
        graph.setdefault(child,[]).append((parent,T)); graph.setdefault(parent,[]).append((child,inverse))
    for node in graph:
        seen=set(); current=node
        while current in parents:
            if current in seen: raise ValueError("Frame cycle")
            seen.add(current); current=parents[current]
    if source not in graph or target not in graph: raise ValueError("Unknown query frame")
    stack=[(source,np.eye(4))]; seen=set()
    while stack:
        node,T=stack.pop()
        if node==target: return T.copy()
        if node in seen: continue
        seen.add(node)
        for neighbor,edge in graph[node]:
            if neighbor not in seen: stack.append((neighbor,edge@T))
    raise ValueError("Disconnected frames")
```
