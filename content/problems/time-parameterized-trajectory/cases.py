import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    q,v=m.sample_trajectory([0,1,3],[[0],[2],[4]],[.5,1,3]); assert_allclose(q,[[1],[2],[4]]); assert_allclose(v,[[2],[1],[1]])
def vector(m):
    q,v=m.sample_trajectory([0,2],[[0,2],[4,0]],[2,0]); assert_allclose(q,[[4,0],[0,2]]); assert_allclose(v,[[2,-1],[2,-1]])
def linear_oracle(m):
    times=np.array([0.,.4,2,9]); positions=times[:,None]*np.array([2.,-3])+[1,4]; old=positions.copy(); query=np.linspace(0,9,501)
    q,v=m.sample_trajectory(times,positions,query); assert_allclose(q,query[:,None]*[2,-3]+[1,4],atol=1e-9)
    assert_allclose(v,np.broadcast_to([2,-3],v.shape)); assert_array_equal(positions,old)
def empty(m):
    q,v=m.sample_trajectory([0,1],[[1],[3]],[]); assert q.shape==v.shape==(0,1); assert q.dtype==v.dtype==np.float64
def invalid(m):
    for args in [([0,0],[[0],[1]],[0]),([0],[[0]],[0]),([0,1],[[0],[1]],[2]),([0,1],[[0],[1]],[-1]),([0,1],[0,1],[0]),([0,1],[[0],[np.nan]],[0])]:
        with np.testing.assert_raises(ValueError): m.sample_trajectory(*args)
TESTS=[('Knot derivative convention','public',example),('Vector and reversed query order','public',vector),('Linear-function oracle','hidden',linear_oracle),('Empty queries','hidden',empty),('Invalid trajectory','hidden',invalid)]

def tiny_denominator(m):
    with np.testing.assert_raises(ValueError): m.sample_trajectory([0,1e-320],[[0],[1]],[0])
TESTS.append(('Reject numerically unsupported denominator','hidden',tiny_denominator))
