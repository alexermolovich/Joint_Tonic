import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def revolute(m):
    assert_allclose(m.geometric_jacobian([[0,0,0]],[[0,0,1]],['R'],[2,0,0])[:,0],[0,2,0,0,0,1])
def prismatic(m):
    assert_allclose(m.geometric_jacobian([[0,0,0]],[[1,0,0]],['P'],[2,0,0])[:,0],[1,0,0,0,0,0])
def finite_motion(m):
    theta=.7; p=np.array([2*np.cos(theta),2*np.sin(theta),0]); eps=1e-6
    derivative=np.array([2*np.cos(theta+eps)-2*np.cos(theta-eps),2*np.sin(theta+eps)-2*np.sin(theta-eps),0])/(2*eps)
    J=m.geometric_jacobian([[0,0,0]],[[0,0,1]],['R'],p); assert_allclose(J[:3,0],derivative,atol=1e-9)
def translation(m):
    o=np.array([[1.,2,3],[2,1,0]]); z=np.array([[0.,1,0],[0,0,-1]]); p=np.array([4.,5,6]); old=o.copy()
    a=m.geometric_jacobian(o,z,['R','P'],p); b=m.geometric_jacobian(o+9,z,['R','P'],p+9); assert_allclose(a,b); assert_array_equal(o,old); assert a.dtype==np.float64
def invalid(m):
    for axes,types in [([[0,0,0]],['R']),([[0,0,2]],['R']),([[0,0,1]],['X']),([[0,0,1]],'R'),([[np.nan,0,1]],['P'])]:
        with np.testing.assert_raises(ValueError): m.geometric_jacobian([[0,0,0]],axes,types,[1,0,0])
TESTS=[('Revolute lever arm','public',revolute),('Prismatic translation','public',prismatic),('Finite-difference geometry oracle','hidden',finite_motion),('Base-origin translation invariance','hidden',translation),('Invalid axes and types','hidden',invalid)]
