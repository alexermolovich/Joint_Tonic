import numpy as np

def _array(x, ndim, kind="f"):
    if not isinstance(x, np.ndarray) or x.ndim != ndim or x.dtype != {"f":np.dtype("float64"),"i":np.dtype("int64"),"b":np.dtype("bool")}[kind]:
        raise ValueError("Invalid array type, dtype or rank")
    if kind == "f" and (not np.isfinite(x).all() or np.any(np.abs(x)>1e6)):
        raise ValueError("Array values must be finite and bounded")
    return x

def _scalar(x, low, high):
    if type(x) not in (int,float) or not low<=x<=high or not np.isfinite(x):raise ValueError("scalar contract")
    return float(x)

def associate_planes(queries,map_points,neighbors,max_neighbor_distance,plane_tolerance):
    q=_array(queries,2);p=_array(map_points,2);k=neighbors;radius=_scalar(max_neighbor_distance,1e-6,1e6);tol=_scalar(plane_tolerance,0,100)
    if q.shape[1]!=3 or p.shape[1]!=3 or len(q)>256 or not 3<=len(p)<=4096 or len(q)*len(p)>1000000 or type(k) is not int or not 3<=k<=min(16,len(p)):raise ValueError("local map contract")
    n=len(q);ids=np.empty((n,k),np.int64);centers=np.empty((n,3));normals=np.full((n,3),np.nan);offsets=np.full(n,np.nan);valid=np.zeros(n,bool)
    for i in range(n):
        squared=np.sum((p-q[i])**2,axis=1);selected=np.argsort(squared,kind="stable")[:k];ids[i]=selected;points=p[selected];center=points.mean(axis=0);centers[i]=center;delta=points-center;values,vectors=np.linalg.eigh(delta.T@delta/k);normal=vectors[:,0]
        if normal[np.argmax(np.abs(normal))]<0:normal=-normal
        good=bool(np.all(squared[selected]<=radius*radius) and values[1]>1e-8 and values[1]-values[0]>1e-8 and np.max(np.abs(delta@normal))<=tol)
        if good:valid[i]=True;normals[i]=normal;offsets[i]=-np.dot(normal,center)
    return dict(neighbor_indices=ids,centroids=centers,normals=normals,offsets=offsets,valid=valid)
