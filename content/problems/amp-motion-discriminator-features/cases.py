import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def fixture(b=1,j=1,e=1):
    return [np.zeros((b,2,3)),np.zeros((b,2)),np.zeros((b,2,3)),np.zeros((b,2,3)),np.tile(np.eye(3),(b,2,j,1,1)),np.zeros((b,2,j,3)),np.tile([1.,0,0],(b,2,e,1))]
def identity(m):
    expected=[0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0];assert_array_equal(m.motion_features(*fixture()),[expected*2])
def heading(m):
    a=fixture();a[1][:]=np.pi/2;a[2][...,2]=-1;r=m.motion_features(*a);assert_allclose(r[0,:3],[1,0,0],atol=1e-12);assert_allclose(r[0,15:18],[0,0,1],atol=1e-12)
    a[0]+=np.array([7,2,-3]);a[6]+=np.array([7,2,-3]);assert_allclose(m.motion_features(*a),r,atol=1e-12)
def order(m):
    a=fixture();a[1][0,1]=np.pi/2;a[2][0,1]=[0,0,-2];r=m.motion_features(*a);assert_allclose(r[0,18:21],[2,0,0],atol=1e-12)
    a=fixture();a[4][0,0,0]=np.array([[0,-1,0],[1,0,0],[0,0,1]]);r=m.motion_features(*a);assert_array_equal(r[0,6:12],[0,1,0,-1,0,0])
def scale(m):
    a=fixture(64,32,8);a[2]=np.zeros((64,2,6))[:,:,::2];r=m.motion_features(*a);assert r.shape==(64,2*(6+9*32+3*8));assert not np.shares_memory(r,a[4]);assert_array_equal(a[4],np.tile(np.eye(3),(64,2,32,1,1)))
def invalid(m):
    a=fixture();a[4][0,0,0,0,0]=-1;bad(lambda:m.motion_features(*a))
    a=fixture();a[1][0,0]=4;bad(lambda:m.motion_features(*a))
    a=fixture();a[3]=np.zeros((1,1,3));bad(lambda:m.motion_features(*a))
TESTS=[('Identity feature layout','public',identity),('Heading and translation invariance','public',heading),('Per-state frame and rotation columns','hidden',order),('Scale fresh feature vectors','hidden',scale),('Invalid frames and shapes','hidden',invalid)]
