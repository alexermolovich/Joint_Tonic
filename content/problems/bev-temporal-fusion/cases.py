import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def args():return np.array([[[2.,4.]]]),np.array([[[10.,0.]]]),np.array([[True]]),np.array([[.25]])
def example(m):assert_allclose(m.fuse_bev(*args(),False),[[[4,3]]])
def reset(m):assert_allclose(m.fuse_bev(*args(),True),[[[2,4]]])
def masks(m):
    x=np.arange(24.).reshape(2,3,4);h=x+8;v=np.array([[True,False,True],[False,True,True]]);g=np.array([[0.,1.,1.],[.5,.25,.75]])
    y=m.fuse_bev(x,h,v,g,False)
    for i in range(2):
        for j in range(3):assert_allclose(y[i,j],x[i,j]+(8*g[i,j] if v[i,j] else 0))
def invalid(m):
    x,h,v,g=args()
    for values in [(x,h,v,g,1),(x,h,v,g*5,False),(x,h,v.astype(np.int64),g,False),(x,h[:,:,:1],v,g,True)]:
        with np.testing.assert_raises(ValueError):m.fuse_bev(*values)
    h[0,0,0]=np.nan
    with np.testing.assert_raises(ValueError):m.fuse_bev(x,h,v,g,True)
def storage(m):
    x,h,v,g=args();saved=x.copy();y=m.fuse_bev(x,h,v,g,False);assert_array_equal(x,saved)
    assert y.dtype==np.float64
    for z in (x,h,v,g):assert not np.shares_memory(y,z)
TESTS=[('Convex blend','public',example),('Sequence reset','public',reset),('Gate endpoints and validity','hidden',masks),('Validation even when ignored','hidden',invalid),('Independent output','hidden',storage)]
