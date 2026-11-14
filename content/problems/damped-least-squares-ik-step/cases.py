import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def singular(m):
    q,r=m.damped_ik_step([[1,0],[0,0]],[2,3],1); assert_allclose(q,[1,0]); assert_allclose(r,[-1,-3])
def redundant(m):
    q,r=m.damped_ik_step([[1,1]],[2],1); assert_allclose(q,[2/3,2/3]); assert_allclose(r,[-2/3])
def optimality(m):
    rng=np.random.default_rng(13); J=rng.normal(size=(5,3)); e=rng.normal(size=5); old=J.copy(); q,r=m.damped_ik_step(J,e,.3)
    assert_allclose(J.T@r+.09*q,0,atol=1e-9); assert_array_equal(J,old); assert q.dtype==r.dtype==np.float64
def zero_and_scale(m):
    q,r=m.damped_ik_step(np.zeros((2,3)),[1,2],.01); assert_array_equal(q,[0,0,0]); assert_array_equal(r,[-1,-2])
    q,r=m.damped_ik_step(np.diag([1,.001]),[1,1],.1); assert_allclose(q,[1/1.01,.001/.010001])
def invalid(m):
    for args in [([[1]],[1],0),([[1]],[1],-1),([[1]],[1],[1]),([1],[1],1),([[1]],[1,2],1),([[np.nan]],[1],1)]:
        with np.testing.assert_raises(ValueError): m.damped_ik_step(*args)
TESTS=[('Singular task direction','public',singular),('Redundant minimum-norm motion','public',redundant),('Regularized normal equation','hidden',optimality),('Zero and near-singular Jacobians','hidden',zero_and_scale),('Invalid regularization','hidden',invalid)]

def tiny_denominator(m):
    with np.testing.assert_raises(ValueError): m.damped_ik_step([[0]],[1],1e-300)
TESTS.append(('Reject numerically unsupported denominator','hidden',tiny_denominator))
