# Solution

Keep the first inlier feature for each landmark ID, count its image cells, then rank eligible candidates. O(KN log N+K log K) time using sorted uniqueness; O(N+K) working memory.

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

def relocalization_coverage(keypoints,landmark_ids,inliers,image_size,grid_size,min_landmarks,min_cells):
    uv=_array(keypoints,2);ids=_array(landmark_ids,2,"i");mask=_array(inliers,2,"b");size=_array(image_size,1,"i");grid=_array(grid_size,1,"i");n=len(uv);k=len(ids)
    if uv.shape!=(n,2) or n>4096 or not 1<=k<=128 or ids.shape!=(k,n) or mask.shape!=(k,n) or size.shape!=(2,) or grid.shape!=(2,) or np.any((size<1)|(size>4096)) or np.any((grid<1)|(grid>64)) or np.any((ids<-1)|(ids>1000000000)) or np.any(mask&(ids<0)):raise ValueError("relocalization evidence contract")
    if np.any(uv<0) or np.any(uv>size[::-1]-1) or type(min_landmarks) is not int or not 1<=min_landmarks<=4096 or type(min_cells) is not int or not 1<=min_cells<=int(grid.prod()):raise ValueError("coverage domain contract")
    cells=np.floor(uv*grid[::-1]/size[::-1]).astype(np.int64);cell_ids=cells[:,1]*grid[1]+cells[:,0];counts=np.zeros(k,np.int64);coverage=np.zeros(k,np.int64)
    for row in range(k):
        features=np.flatnonzero(mask[row]);_,first=np.unique(ids[row,features],return_index=True);representatives=features[first];counts[row]=len(representatives);coverage[row]=len(np.unique(cell_ids[representatives]))
    eligible=(counts>=min_landmarks)&(coverage>=min_cells);candidates=np.flatnonzero(eligible);order=candidates[np.lexsort((candidates,-coverage[candidates],-counts[candidates]))]
    return dict(unique_landmarks=counts,covered_cells=coverage,eligible=eligible,order=order,best=int(order[0]) if len(order) else -1)
```
