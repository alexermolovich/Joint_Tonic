import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    x,p=m.kalman_update([0],[[1]],[2],[[1]],[[1]]); assert_allclose(x,[1]); assert_allclose(p,[[.5]])
def known(m):
    x,p=m.kalman_update([3],[[0]],[10],[[1]],[[2]]); assert_allclose(x,[3]); assert_array_equal(p,[[0]])
def correlated(m):
    P=np.array([[2.,1],[1,3]]); original=P.copy(); x,p=m.kalman_update([0,0],P,[3],[[1,0]],[[1]])
    assert_allclose(x,[2,1]); assert_allclose(p,[[2/3,1/3],[1/3,8/3]],atol=1e-9); assert_array_equal(P,original)
    assert np.linalg.eigvalsh(p).min()>0 and x.dtype==p.dtype==np.float64
def information_oracle(m):
    P=np.diag([2.,3]); H=np.array([[1.,2],[0,1]]); R=np.diag([.5,2]); x=np.array([1.,-1]); z=np.array([3.,2])
    mean,cov=m.kalman_update(x,P,z,H,R)
    expected=np.linalg.inv(np.linalg.inv(P)+H.T@np.linalg.inv(R)@H)
    assert_allclose(cov,expected); assert_allclose(mean,expected@(np.linalg.solve(P,x)+H.T@np.linalg.solve(R,z)))
def invalid(m):
    for r in [[[0]],[[-1]],[[np.nan]],[[True]]]:
        with np.testing.assert_raises(ValueError): m.kalman_update([0],[[1]],[1],[[1]],r)
    with np.testing.assert_raises(ValueError): m.kalman_update([0],[[1]],[1,2],[[1]],[[1]])
    with np.testing.assert_raises(ValueError): m.kalman_update([0],[[-1]],[1],[[1]],[[1]])
TESTS=[('Equal-confidence fusion','public',example),('Known prior','public',known),('Correlated state correction','hidden',correlated),('Independent information-form oracle','hidden',information_oracle),('Invalid observations','hidden',invalid)]

def tolerated_negative_covariance(m):
    x,p=m.kalman_update([0],[[-5e-11]],[1],[[2]],[[2e-10]])
    assert_allclose(x,[0],atol=1e-15); assert_allclose(p,[[0]],atol=1e-15)
TESTS.append(('Project tolerated negative eigenvalue','hidden',tolerated_negative_covariance))
