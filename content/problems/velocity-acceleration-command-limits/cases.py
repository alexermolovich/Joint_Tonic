import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    q,v=m.limit_joint_commands([0],[0],[[10],[10],[10]],1,[2],[1]); assert_allclose(q,[[1],[3],[5]]); assert_allclose(v,[[1],[2],[2]])
def braking(m):
    q,v=m.limit_joint_commands([0],[2],[[-10]],1,[2],[1]); assert_allclose(q,[[1]]); assert_allclose(v,[[1]])
def constraints(m):
    rng=np.random.default_rng(13); goals=rng.normal(size=(200,3))*10; old=goals.copy(); vmax=np.array([1,2,3]); amax=np.array([.1,.3,.7]); dt=.2
    q,v=m.limit_joint_commands([0,0,0],[0,0,0],goals,dt,vmax,amax)
    assert np.all(np.abs(v)<=vmax+1e-9); assert np.all(np.abs(np.diff(np.vstack([np.zeros(3),v]),axis=0))<=amax*dt+1e-9)
    assert_allclose(np.diff(np.vstack([np.zeros(3),q]),axis=0),v*dt,atol=1e-9); assert_array_equal(goals,old)
def exact_and_empty(m):
    q,v=m.limit_joint_commands([0,0],[0,0],[[.1,-.2]],1,[2,2],[1,1]); assert_allclose(q,[[.1,-.2]]); assert_allclose(v,q)
    q,v=m.limit_joint_commands([0],[0],np.empty((0,1)),1,[1],[1]); assert q.shape==v.shape==(0,1) and q.dtype==np.float64
def invalid(m):
    for args in [([0],[2],[[0]],1,[1],[1]),([0],[0],[[0]],0,[1],[1]),([0],[0],[[0]],1,[0],[1]),([0],[0],[[0]],1,[1],[-1]),([0],[0],[[np.nan]],1,[1],[1]),([0],[0],[[0,1]],1,[1],[1])]:
        with np.testing.assert_raises(ValueError): m.limit_joint_commands(*args)
TESTS=[('Acceleration ramp then speed cap','public',example),('Bounded braking','public',braking),('Physical limits and integration invariants','hidden',constraints),('Reachable and empty commands','hidden',exact_and_empty),('Invalid limits','hidden',invalid)]

def tiny_denominator(m):
    with np.testing.assert_raises(ValueError): m.limit_joint_commands([0],[0],[[1]],1e-320,[1],[1])
TESTS.append(('Reject numerically unsupported denominator','hidden',tiny_denominator))
