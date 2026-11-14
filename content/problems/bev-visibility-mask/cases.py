import numpy as np
from numpy.testing import assert_array_equal
def example(m):assert_array_equal(m.bev_visibility(np.array([[[0.,0],[4,2],[3.9,2.9]]]),np.ones((1,3)),np.array([[3,4]],dtype=np.int64)),[[True,False,True]])
def depths(m):assert_array_equal(m.bev_visibility(np.ones((1,3,2)),np.array([[-1.,1e-6,2e-6]]),np.array([[2,2]],dtype=np.int64)),[[False,False,True]])
def camera_sizes(m):
    u=np.array([[[2.,3],[-1e-9,0],[0,-1e-9]],[[2.,3],[0,0],[1,1]]]);z=np.ones((2,3));s=np.array([[4,3],[3,2]],dtype=np.int64)
    assert_array_equal(m.bev_visibility(u,z,s),[[True,False,False],[False,True,True]])
def empty(m):assert m.bev_visibility(np.empty((2,0,2)),np.empty((2,0)),np.ones((2,2),dtype=np.int64)).shape==(2,0)
def invalid(m):
    for u,z,s in [(np.ones((1,1,2)),np.ones((1,1)),np.zeros((1,2),dtype=np.int64)),(np.ones((1,1,2)),np.ones((1,2)),np.ones((1,2),dtype=np.int64)),(np.ones((1,1,2)),np.ones((1,1)),np.ones((1,2)))]:
        with np.testing.assert_raises(ValueError):m.bev_visibility(u,z,s)
def preservation(m):
    u=np.ones((2,8,2))[:,::2];z=np.ones((2,4));s=np.array([[3,5],[1,1]],dtype=np.int64);copy=u.copy();v=m.bev_visibility(u,z,s);assert v.dtype==np.bool_;assert_array_equal(u,copy)
TESTS=[('Image bounds','public',example),('Depth cutoff','public',depths),('Per-camera bounds','hidden',camera_sizes),('Empty points','hidden',empty),('Validation','hidden',invalid),('Noncontiguous input','hidden',preservation)]
