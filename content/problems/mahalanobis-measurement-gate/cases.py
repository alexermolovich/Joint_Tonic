import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    d,a=m.gate_measurements([[2,0],[0,2]],np.diag([4,1]),1); assert_allclose(d,[1,4]); assert_array_equal(a,[True,False])
def zero(m):
    d,a=m.gate_measurements([[0]],[[2]],0); assert_array_equal(d,[0]); assert_array_equal(a,[True])
def correlated(m):
    S=np.array([[2.,1],[1,2]]); r=np.array([[1.,1],[1,-1]]); old=r.copy(); d,a=m.gate_measurements(r,S,1)
    assert_allclose(d,[2/3,2]); assert_array_equal(a,[1,0]); assert_array_equal(r,old)
def whitening(m):
    rng=np.random.default_rng(13); L=np.tril(rng.normal(size=(4,4)))+5*np.eye(4); r=rng.normal(size=(100,4)); d,_=m.gate_measurements(r,L@L.T,2)
    assert_allclose(d,np.sum(np.linalg.solve(L,r.T)**2,axis=0)); assert d.dtype==np.float64
    d,a=m.gate_measurements(np.empty((0,4)),np.eye(4),1); assert d.shape==a.shape==(0,) and a.dtype==bool
def invalid(m):
    for args in [([[0]],[[0]],1),([[0]],[[-1]],1),([[0]],[[1]],-1),([0],[[1]],1),([[True]],[[1]],1),([[0]],[[np.inf]],1),([[0]],[[1]],[1])]:
        with np.testing.assert_raises(ValueError): m.gate_measurements(*args)
TESTS=[('Anisotropic gate','public',example),('Zero-threshold equality','public',zero),('Correlation matters','hidden',correlated),('Whitened oracle and empty batch','hidden',whitening),('Invalid gate contract','hidden',invalid)]
