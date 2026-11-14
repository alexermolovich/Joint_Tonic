import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def args(): return ([1,1],[[0,0],[np.pi/2,0]],[[-np.pi,np.pi],[-np.pi,np.pi]])
def clear(m):
    r=m.select_safe_ik_candidate(*args(),np.empty((0,3)),[2,0],0); assert r['index']==0 and r['error']==0; assert_allclose(r['point'],[2,0])
def blocked(m):
    r=m.select_safe_ik_candidate(*args(),[[.5,0,.1]],[2,0],0); assert r['index']==1; assert_allclose(r['point'],[0,2],atol=1e-9); assert_allclose(r['error'],np.sqrt(8))
def contact_and_limits(m):
    # Circle tangent to first link and endpoint obstacle must both reject.
    for obs in [[[.5,.25,.25]],[[2,0,0]]]: assert m.select_safe_ik_candidate([1,1],[[0,0]],[[-1,1],[-1,1]],obs,[2,0],0) is None
    assert m.select_safe_ik_candidate([1,1],[[.1,0]],[[0,0],[-1,1]],np.empty((0,3)),[2,0],0) is None
def ties_and_empty(m):
    q=np.zeros((2,2)); old=q.copy(); r=m.select_safe_ik_candidate([1,1],q,[[-1,1],[-1,1]],np.empty((0,3)),[2,0],0)
    assert r['index']==0 and isinstance(r['index'],int); assert set(r)=={'index','q','point','error'}; assert not np.shares_memory(r['q'],q); assert_array_equal(q,old)
    assert m.select_safe_ik_candidate([1,1],np.empty((0,2)),[[-1,1],[-1,1]],np.empty((0,3)),[2,0],0) is None
def invalid(m):
    for obs in [[[0,0,-1]],[[0,0,np.nan]],[]]:
        with np.testing.assert_raises(ValueError): m.select_safe_ik_candidate(*args(),obs,[2,0],0)
    with np.testing.assert_raises(ValueError): m.select_safe_ik_candidate(*args(),np.empty((0,3)),[2,0],-1)
TESTS=[('Closest feasible candidate','public',clear),('Link collision changes choice','public',blocked),('Touch and joint-boundary policies','hidden',contact_and_limits),('Tie ordering and empty candidates','hidden',ties_and_empty),('Invalid obstacles','hidden',invalid)]

def tiny_denominator(m):
    with np.testing.assert_raises(ValueError): m.select_safe_ik_candidate([1e-300,1],[[0,0]],[[-1,1],[-1,1]],np.empty((0,3)),[1,0],0)
TESTS.append(('Reject numerically unsupported denominator','hidden',tiny_denominator))
