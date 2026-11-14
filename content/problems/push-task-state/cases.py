import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
 r=m.push_task_state(np.array([3.,4]),np.array([[1.,2],[0,1]]),np.array([2.,-1]));assert_array_equal(r['position'],[3,4]);assert_array_equal(r['velocity'],[0,-1])
def second(m):
 x=np.array([1.]);r=m.push_task_state(x,np.array([[2.,3]]),np.zeros(2));assert_array_equal(r['velocity'],[0]);assert not np.shares_memory(r['position'],x)
def oracle(m):
 rng=np.random.default_rng(816);x=rng.normal(size=32)[::2];j=rng.normal(size=(16,32))[:,::2];v=rng.normal(size=32)[::2];before=[x.copy(),j.copy(),v.copy()];r=m.push_task_state(x,j,v)
 assert_allclose(r['velocity'],[sum(float(j[i,k])*float(v[k]) for k in range(16)) for i in range(16)],atol=1e-12)
 for a,b in zip(before,[x,j,v]):assert_array_equal(a,b)
 assert not np.shares_memory(r['velocity'],v)
def rank_deficient(m):
 r=m.push_task_state(np.zeros(2),np.array([[1.,1],[2,2]]),np.array([1.,-1]));assert_array_equal(r['velocity'],[0,0])
def invalid(m):
 for x,j,v in [(np.zeros(0),np.zeros((0,1)),np.ones(1)),(np.ones(1),np.ones((2,1)),np.ones(1)),(np.ones(1),np.ones((1,1),dtype=np.float32),np.ones(1)),(np.ones(1),np.ones((1,1)),np.array([np.nan]))]:bad(lambda:m.push_task_state(x,j,v))
TESTS=[('Coupled task velocity','public',first),('Stationary state','public',second),('Scalar oracle and noncontiguous scale','hidden',oracle),('Nullspace velocity','hidden',rank_deficient),('Invalid task contract','hidden',invalid)]
