import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    p,q=m.interpolate_pose([0,0,0],[1,0,0,0],[2,0,0],[0,0,0,1],.5); assert_allclose(p,[1,0,0]); assert_allclose(q,[np.sqrt(.5),0,0,np.sqrt(.5)],atol=1e-9)
def antipodal(m):
    p,q=m.interpolate_pose([0,0,0],[2,0,0,0],[2,0,0],[-3,0,0,0],.5); assert_allclose(q,[1,0,0,0])
def angular_oracle(m):
    end=np.array([np.cos(.8),0,np.sin(.8),0]); old=end.copy()
    for u in [0,.1,.4,.9,1]:
        p,q=m.interpolate_pose([1,2,3],[1,0,0,0],[3,4,5],end,u); assert_allclose(q,[np.cos(.8*u),0,np.sin(.8*u),0],atol=1e-9); assert_allclose(p,[1+2*u,2+2*u,3+2*u])
    assert_array_equal(end,old)
def tiny_and_near(m):
    _,q=m.interpolate_pose([0,0,0],[1e-300,0,0,0],[0,0,0],[1,1e-6,0,0],.5)
    b=np.array([1,1e-6,0,0]); b/=np.linalg.norm(b); expected=(np.array([1,0,0,0])+b)/2; expected/=np.linalg.norm(expected)
    assert_allclose(q,expected,atol=1e-12); assert q.dtype==np.float64
def invalid(m):
    for q,u in [([0,0,0,0],.5),([1,0,0],.5),([1,0,0,0],1.1),([1,0,0,0],[.5]),([np.nan,0,0,0],.5)]:
        with np.testing.assert_raises(ValueError): m.interpolate_pose([0,0,0],q,[1,0,0],[1,0,0,0],u)
TESTS=[('Half-turn midpoint','public',example),('Quaternion double cover','public',antipodal),('Known angular path','hidden',angular_oracle),('Tiny normalization and near-equal branch','hidden',tiny_and_near),('Invalid poses','hidden',invalid)]
