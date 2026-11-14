# Solution

Build the output center grid once. For each supplied warp, project and bilinearly sample supported points, accumulating sums and counts. O(K*output_height*output_width) time and O(output_height*output_width) working memory beyond the returned arrays.

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

def _homography(h):
    if h.shape[-2:]!=(3,3) or np.any(np.abs(h)>1000) or np.any(np.abs(np.linalg.det(h))<1e-9):raise ValueError("homography contract")
    return h

def _project(points,h):
    homogeneous=np.column_stack([points,np.ones(len(points))])@h.T;valid=np.abs(homogeneous[:,2])>1e-9
    uv=np.full((len(points),2),np.nan);uv[valid]=homogeneous[valid,:2]/homogeneous[valid,2,None]
    return uv,valid

def _size(size):
    size=_array(size,1,"i")
    if size.shape!=(2,) or np.any((size<1)|(size>4096)):raise ValueError("image size")
    return size

def _inside(p,size):
    return (p[:,0]>=0)&(p[:,0]<=size[1]-1)&(p[:,1]>=0)&(p[:,1]<=size[0]-1)

def _sample(image,points):
    h,w=image.shape[:2];inside=(points[:,0]>=0)&(points[:,0]<=w-1)&(points[:,1]>=0)&(points[:,1]<=h-1);out=np.zeros((len(points),)+image.shape[2:])
    xy=points[inside];lo=np.floor(xy).astype(np.int64);hi=np.minimum(lo+1,[w-1,h-1]);f=xy-lo
    for i,j in ((0,0),(1,0),(0,1),(1,1)):
        x=hi[:,0] if i else lo[:,0];y=hi[:,1] if j else lo[:,1];weight=(f[:,0] if i else 1-f[:,0])*(f[:,1] if j else 1-f[:,1])
        out[inside]+=image[y,x]*weight.reshape((-1,)+(1,)*(image.ndim-2))
    return out,inside

def adapt_keypoints(probabilities,homographies,output_size):
    p=_array(probabilities,3);h=_array(homographies,3);size=_size(output_size);k,height,width=p.shape
    if not 1<=k<=16 or not 1<=height<=256 or not 1<=width<=256 or p.size>1000000 or np.any((p<0)|(p>1)) or h.shape!=(k,3,3) or np.any(size>256):raise ValueError("adaptation contract")
    _homography(h);y,x=np.indices(tuple(size));points=np.column_stack([x.ravel(),y.ravel()]);total=np.zeros(len(points));count=np.zeros(len(points),dtype=np.int64)
    for image,transform in zip(p,h):
        uv,projected=_project(points,transform);sampled,inside=_sample(image,uv);valid=projected&inside;total[valid]+=sampled[valid];count+=valid
    average=np.divide(total,count,out=np.full(len(points),np.nan),where=count>0)
    return dict(probability=average.reshape(tuple(size)),count=count.reshape(tuple(size)))
```
