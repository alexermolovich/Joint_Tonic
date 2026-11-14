import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    x,p=m.kalman_predict([0,2],np.eye(2),[[1,1],[0,1]],np.diag([.1,.2])); assert_allclose(x,[2,2]); assert_allclose(p,[[2.1,1],[1,1.2]])
def scalar(m):
    x,p=m.kalman_predict([3],[[2]],[[1]],[[0]]); assert_allclose(x,[3]); assert_allclose(p,[[2]])
def transported_samples(m):
    F=np.array([[2.,-1],[.5,3]]); deviations=np.array([[1,0],[-1,0],[0,2],[0,-2.]])
    P=deviations.T@deviations/4; old=P.copy(); x,p=m.kalman_predict([1,-2],P,F,np.zeros((2,2)))
    transported=deviations@F.T; assert_allclose(p,transported.T@transported/4)
    assert_allclose(x,[4,-5.5]); assert_array_equal(P,old); assert x.dtype==p.dtype==np.float64
def zero(m):
    x,p=m.kalman_predict(np.zeros(32),np.zeros((32,32)),np.eye(32),np.eye(32)); assert_array_equal(p,np.eye(32))
def invalid(m):
    for x,p,f,q in [([],[],[],[]),([0],[[1]],[[1]],[[ -1]]),([0,0],[[1,2],[0,1]],np.eye(2),np.eye(2)),([0],[[1]],[[np.nan]],[[1]]),([True],[[1]],[[1]],[[1]]),([0],[[1]],[[1,2]],[[1]])]:
        with np.testing.assert_raises(ValueError): m.kalman_predict(x,p,f,q)
TESTS=[('Position velocity prediction','public',example),('Identity interval','public',scalar),('Transported ensemble covariance','hidden',transported_samples),('Zero uncertainty and max dimension','hidden',zero),('Invalid covariance and shape','hidden',invalid)]
