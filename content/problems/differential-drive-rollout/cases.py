import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def straight(m):
    assert_allclose(m.differential_drive_rollout([0,0,0],[[1,1],[1,1]],1,1,2),[[0,0,0],[1,0,0],[2,0,0]],atol=1e-9)
def turn(m):
    assert_allclose(m.differential_drive_rollout([0,0,0],[[0,2]],1,1,2)[-1],[np.sin(1),1-np.cos(1),1],atol=1e-9)
def composition(m):
    pose=np.array([2.,3.,.7]); old=pose.copy()
    once=m.differential_drive_rollout(pose,[[.3,1.2]],2,.4,.8)[-1]
    split=m.differential_drive_rollout(pose,np.tile([.3,1.2],(20,1)),.1,.4,.8)[-1]
    assert_allclose(once,split,atol=1e-9); assert_array_equal(pose,old)
def stationary(m):
    out=m.differential_drive_rollout([1,2,0],[[-1,1]],np.pi,1,2); assert_allclose(out[-1],[1,2,-np.pi],atol=1e-9)
    empty=m.differential_drive_rollout([1,2,2*np.pi],np.empty((0,2)),1,1,2); assert_allclose(empty,[[1,2,0]],atol=1e-9); assert empty.dtype==np.float64
def invalid(m):
    for args in [([0,0],[[1,1]],1,1,2),([0,0,0],[1,1],1,1,2),([0,0,0],[[1,1]],0,1,2),([0,0,0],[[1,1]],1,-1,2),([0,0,0],[[np.nan,1]],1,1,2)]:
        with np.testing.assert_raises(ValueError): m.differential_drive_rollout(*args)
TESTS=[('Straight motion','public',straight),('Exact circular arc','public',turn),('Time subdivision invariance','hidden',composition),('In-place turn and empty input','hidden',stationary),('Invalid drive contract','hidden',invalid)]

def tiny_denominator(m):
    with np.testing.assert_raises(ValueError): m.differential_drive_rollout([0,0,0],[[0,1]],1,1,1e-320)
TESTS.append(('Reject numerically unsupported denominator','hidden',tiny_denominator))
