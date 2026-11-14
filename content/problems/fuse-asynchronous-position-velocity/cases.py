import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    x,p=m.fuse_async_sensors([0,0],np.eye(2),0,[[0,0,2],[0,1,4]],[1,1],0)
    assert_allclose(x,[[1,0],[1,2]]); assert_allclose(p,[np.diag([.5,1]),np.diag([.5,.5])])
def movement(m):
    x,p=m.fuse_async_sensors([0,1],np.zeros((2,2)),0,[[2,0,2]],[1],0)
    assert_allclose(x,[[2,1]]); assert_array_equal(p,np.zeros((1,2,2)))
def process_noise(m):
    x,p=m.fuse_async_sensors([0,0],np.zeros((2,2)),0,[[3,1,2]],[2],2)
    # Prior Q=[[18,9],[9,6]], velocity gain=[9,6]/8.
    assert_allclose(x,[[2.25,1.5]]); assert_allclose(p,[[[7.875,2.25],[2.25,1.5]]])
def empty_and_repeat(m):
    initial=np.array([1.,2]); old=initial.copy()
    x,p=m.fuse_async_sensors(initial,np.eye(2),0,np.empty((0,3)),[],0)
    assert x.shape==(0,2) and p.shape==(0,2,2); assert_array_equal(initial,old)
    x,p=m.fuse_async_sensors([0,0],np.eye(2),0,[[0,0,3],[0,0,3]],[1,1],0)
    assert_allclose(x[:,0],[1.5,2]); assert_allclose(p[-1],np.diag([1/3,1]))
def invalid(m):
    for events,var in [([[1,0,0],[0,1,0]],[1,1]),([[-1,0,0]],[1]),([[0,2,0]],[1]),([[0,0,0]],[0]),([[0,0,0]],[]),([[0,0,np.nan]],[1])]:
        with np.testing.assert_raises(ValueError): m.fuse_async_sensors([0,0],np.eye(2),0,events,var,0)
    with np.testing.assert_raises(ValueError): m.fuse_async_sensors([0,0],np.eye(2),0,np.empty((0,3)),[],-1)
TESTS=[('Two simultaneous sensors','public',example),('Predict across time','public',movement),('Continuous process noise','hidden',process_noise),('Empty and repeated observations','hidden',empty_and_repeat),('Invalid event contract','hidden',invalid)]
