# Solution

Project map points, search a bounded pixel neighborhood, count differing descriptor bits, and choose one proposal per landmark. Sort proposals once to resolve feature collisions. O(MF*32+M log M) time and O(F*32+M) working memory.

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

def _rotation(r):
    if r.shape[-2:]!=(3,3) or not np.allclose(r.swapaxes(-1,-2)@r,np.eye(3),atol=1e-9,rtol=0) or not np.allclose(np.linalg.det(r),1,atol=1e-9,rtol=0):raise ValueError("proper rotation required")
    return r

def _transform(t):
    if t.shape[-2:]!=(4,4) or not np.allclose(t[...,3,:],[0,0,0,1],atol=1e-9,rtol=0):raise ValueError("rigid transform required")
    _rotation(t[...,:3,:3]);return t

def _intrinsics(k):
    if k.shape!=(4,) or np.any(k[:2]<1e-3):raise ValueError("camera intrinsics contract")
    return k

def associate_map_features(world_points,map_descriptors,keypoints,image_descriptors,camera_from_world,intrinsics,radius,max_hamming):
    p=_array(world_points,2);uv=_array(keypoints,2);t=_array(camera_from_world,2);k=_array(intrinsics,1);rad=_scalar(radius,0,100);limit=max_hamming;m=len(p);n=len(uv)
    if p.shape!=(m,3) or uv.shape!=(n,2) or m>512 or n>512 or t.shape!=(4,4) or type(limit) is not int or not 0<=limit<=256:raise ValueError("association shape contract")
    for desc,rows in [(map_descriptors,m),(image_descriptors,n)]:
        if not isinstance(desc,np.ndarray) or desc.dtype!=np.uint8 or desc.shape!=(rows,32):raise ValueError("packed uint8 descriptor contract")
    _transform(t);_intrinsics(k);camera=p@t[:3,:3].T+t[:3,3];proposals=[]
    for i in range(m):
        if camera[i,2]<=1e-6:continue
        projected=camera[i,:2]/camera[i,2]*k[:2]+k[2:];distance=np.sum((uv-projected)**2,axis=1);ids=np.flatnonzero(distance<=rad*rad)
        if not len(ids):continue
        ham=np.unpackbits(np.bitwise_xor(image_descriptors[ids],map_descriptors[i]),axis=1).sum(axis=1);good=ham<=limit;ids=ids[good];ham=ham[good]
        if not len(ids):continue
        chosen=int(np.lexsort((ids,distance[ids],ham))[0]);j=int(ids[chosen]);proposals.append((int(ham[chosen]),float(distance[j]),i,j))
    indices=np.full(m,-1,np.int64);hamming=np.full(m,-1,np.int64);error=np.full(m,np.inf);used=set()
    for ham,dist,i,j in sorted(proposals):
        if j not in used:used.add(j);indices[i]=j;hamming[i]=ham;error[i]=dist
    return dict(feature_indices=indices,hamming=hamming,squared_error=error)
```
