import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    p,t=m.planar_forward_kinematics([1,.5],[np.pi/2,-np.pi/2]); assert_allclose(p,[[0,0],[0,1],[.5,1]],atol=1e-9); assert_allclose(t,[[1,0,.5],[0,1,1],[0,0,1]],atol=1e-9)
def one(m):
    p,t=m.planar_forward_kinematics([2],[0]); assert_allclose(p,[[0,0],[2,0]]); assert_allclose(t,[[1,0,2],[0,1,0],[0,0,1]])
def transform_oracle(m):
    rng=np.random.default_rng(13); L=rng.uniform(.1,2,40); q=rng.uniform(-2,2,40); old=q.copy(); p,t=m.planar_forward_kinematics(L,q); expected=np.eye(3)
    for i,(length,angle) in enumerate(zip(L,q)):
        c,s=np.cos(angle),np.sin(angle); expected=expected@np.array([[c,-s,length*c],[s,c,length*s],[0,0,1]])
        assert_allclose(p[i+1],expected[:2,2],atol=1e-9)
    assert_allclose(t,expected,atol=1e-9); assert_array_equal(q,old); assert p.dtype==t.dtype==np.float64
def geometry(m):
    p,t=m.planar_forward_kinematics(np.ones(1000),np.zeros(1000)); assert_allclose(p[-1],[1000,0]); assert_allclose(np.linalg.norm(np.diff(p,axis=0),axis=1),1)
def invalid(m):
    for L,q in [([],[]),([0],[0]),([-1],[0]),([1],[0,1]),([[1]],[0]),([1],[np.nan]),([True],[0])]:
        with np.testing.assert_raises(ValueError): m.planar_forward_kinematics(L,q)
TESTS=[('Relative elbow angle','public',example),('Single link','public',one),('Homogeneous-product oracle','hidden',transform_oracle),('Long straight chain','hidden',geometry),('Invalid geometry','hidden',invalid)]
