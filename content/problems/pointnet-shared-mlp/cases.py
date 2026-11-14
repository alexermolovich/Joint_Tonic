import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def example(m):
    h,g=m.point_mlp(np.array([[1.,2.],[-1.,3.]]),np.eye(2),np.array([0.,-2.]))
    assert_allclose(h,[[1,0],[0,1]]);assert_allclose(g,[1,1])
def minimal(m):
    h,g=m.point_mlp(np.array([[2.]]),np.array([[-3.]]),np.array([1.]))
    assert_allclose(h,[[0]]);assert_allclose(g,[0])
def mechanism(m):
    r=np.random.default_rng(88);p=r.normal(size=(73,7));w=r.normal(size=(7,11));b=r.normal(size=11)
    h,g=m.point_mlp(p,w,b)
    expected=np.array([[max(0,sum(float(p[i,k])*float(w[k,j]) for k in range(7))+b[j]) for j in range(11)] for i in range(73)])
    assert_allclose(h,expected,atol=1e-12);assert_allclose(g,expected.max(0))
    hp,gp=m.point_mlp(p[::-1],w,b);assert_allclose(hp,h[::-1]);assert_allclose(gp,g)
def invalid(m):
    for p,w,b in [(np.empty((0,2)),np.eye(2),np.zeros(2)),(np.ones((2,2),dtype=np.float32),np.eye(2),np.zeros(2)),(np.ones((2,2)),np.eye(3),np.zeros(3)),(np.array([[np.nan]]),np.ones((1,1)),np.zeros(1))]:
        with np.testing.assert_raises(ValueError):m.point_mlp(p,w,b)
def storage(m):
    p=np.arange(24.).reshape(4,6)[:,::2];w=np.ones((3,2));b=np.zeros(2);copies=[x.copy() for x in (p,w,b)]
    h,g=m.point_mlp(p,w,b)
    for x,c in zip((p,w,b),copies):
        assert_array_equal(x,c);assert not np.shares_memory(x,h);assert not np.shares_memory(x,g)
    assert h.dtype==g.dtype==np.float64
TESTS=[('Shared features','public',example),('Single point','public',minimal),('Independent scalar and permutation checks','hidden',mechanism),('Contract validation','hidden',invalid),('Strides and preservation','hidden',storage)]
