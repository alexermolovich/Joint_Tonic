import numpy as np
from numpy.testing import assert_allclose, assert_array_equal


def identity_scaled(m):
    assert_allclose(m.compose_quaternions([2,0,0,0],[0,0,0,3]),[0,0,0,1],atol=1e-9)


def axis_order(m):
    s=np.sqrt(.5)
    assert_allclose(m.compose_quaternions([s,0,0,s],[s,s,0,0]),[.5,.5,.5,.5],atol=1e-9)
    assert_allclose(m.compose_quaternions([s,s,0,0],[s,0,0,s]),[.5,.5,-.5,.5],atol=1e-9)


def sign_and_inverse(m):
    q=np.array([1.,2.,3.,4.]); unit=q/np.linalg.norm(q)
    assert_allclose(m.compose_quaternions([-1,0,0,0],q),-unit,atol=1e-9)
    assert_allclose(m.compose_quaternions([1,-2,-3,-4],q),[1,0,0,0],atol=1e-9)
    assert_allclose(m.compose_quaternions(-q,-q),m.compose_quaternions(q,q),atol=1e-9)


def tiny_and_large(m):
    for scale in [1e-300,1e6]:
        assert_allclose(m.compose_quaternions([scale,0,0,0],[0,scale,0,0]),[0,1,0,0],atol=1e-9)
    out=m.compose_quaternions(np.array([1,0,0,0],np.float32),np.array([1,0,0,0],np.int32))
    assert out.dtype==np.float64 and out.shape==(4,)


def invalid(m):
    bads=[[],[1,0,0],[[1,0,0,0]],[0,0,0,0],[np.nan,0,0,0],[np.inf,0,0,0],
          [True,False,False,False],["1","0","0","0"],[1j,0,0,0],[1000001,0,0,0],np.array([1,0,0,0],object)]
    for bad in bads:
        with np.testing.assert_raises(ValueError): m.compose_quaternions(bad,[1,0,0,0])
        with np.testing.assert_raises(ValueError): m.compose_quaternions([1,0,0,0],bad)


def rotation(q):
    w,x,y,z=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                     [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])


def matrix_composition(m):
    rng=np.random.default_rng(20261113)
    for _ in range(100):
        a,b=rng.normal(size=(2,4)); ac,bc=a.copy(),b.copy()
        result=m.compose_quaternions(a,b)
        assert_allclose(rotation(result),rotation(a/np.linalg.norm(a))@rotation(b/np.linalg.norm(b)),atol=1e-9)
        assert_allclose(np.linalg.norm(result),1,atol=1e-9)
        assert_array_equal(a,ac); assert_array_equal(b,bc)
        assert not np.shares_memory(result,a) and not np.shares_memory(result,b)


TESTS=[("Scaled identity composition","public",identity_scaled),("Two axes and order","public",axis_order),
       ("Product sign and inverse","hidden",sign_and_inverse),("Safe tiny normalization","hidden",tiny_and_large),
       ("Malformed quaternions","hidden",invalid),("Independent rotation-matrix oracle","hidden",matrix_composition)]
