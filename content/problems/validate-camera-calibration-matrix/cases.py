import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def valid(m):
    assert m.validate_camera_matrix([[500,0,320],[0,510,240],[0,0,1]],640,480) is True
def boundary(m):
    assert m.validate_camera_matrix([[500,0,320],[0,510,240],[0,0,1]],320,480) is False
def policies(m):
    K=np.array([[1.,4,0],[0,2,0],[0,0,1]]); old=K.copy(); assert m.validate_camera_matrix(K,1,1); assert_array_equal(K,old)
    for index,value in [((0,0),0),((1,1),-1),((0,2),-1),((1,2),1),((1,0),1e-8),((2,2),2)]:
        bad=K.copy(); bad[index]=value; assert m.validate_camera_matrix(bad,1,1) is False
def tolerance(m):
    K=np.eye(3); K[1,0]=.5e-9; K[2,0]=-.5e-9; assert m.validate_camera_matrix(K,1,1)
def invalid(m):
    for K,w,h in [([[1]],1,1),(np.eye(3),True,1),(np.eye(3),1.,1),(np.eye(3),1,0),(np.full((3,3),np.nan),1,1),(np.eye(3,dtype=bool),1,1)]:
        with np.testing.assert_raises(ValueError): m.validate_camera_matrix(K,w,h)
TESTS=[('Valid intrinsics','public',valid),('Image boundary rejected','public',boundary),('Independent policy failures','hidden',policies),('Structural tolerance','hidden',tolerance),('Malformed matrices','hidden',invalid)]
