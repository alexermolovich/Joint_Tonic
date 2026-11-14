"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import math
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')

def same(a,b):np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)
def f(x):return np.array(x,dtype=np.float64)
def i(x):return np.array(x,dtype=np.int64)
def b(x):return np.array(x,dtype=bool)

def unchanged(before,after):
    for x,y in zip(before,after):np.testing.assert_array_equal(x,y)

def example1(m):
 r=m.reset_environment_batch(f([[1,2],[3,4]]),f([[0,0],[9,9]]),b([True,False]),i([4,8]),i([10,20]));same(r['state'],[[0,0],[3,4]]);same(r['episode_ids'],[5,8]);same(r['steps'],[0,20])
def example2(m):
 hi=np.iinfo(np.int64).max;r=m.reset_environment_batch(f([[3]]),f([[0]]),b([False]),i([hi]),i([7]));assert int(r['episode_ids'][0])==hi;same(r['steps'],[7]);same(r['state'],[[3]])
def edges(m):
 r=m.reset_environment_batch(np.zeros((0,3),dtype=np.float32),np.zeros((0,3)),b([]),i([]),i([]));assert r['state'].shape==(0,3) and r['state'].dtype==np.float64 and r['steps'].dtype==np.int64
 hi=np.iinfo(np.int64).max;r=m.reset_environment_batch(f([[3]]),f([[0]]),b([True]),i([hi-1]),i([hi]));assert int(r['episode_ids'][0])==hi and r['steps'][0]==0
def oracle_scale(m):
 rng=np.random.default_rng(927);x=rng.normal(size=(4096,256))[:,::2];z=np.zeros_like(x);done=np.arange(len(x))%3==0;ids=np.arange(len(x),dtype=np.int64);steps=ids*4;before=[v.copy() for v in [x,z,done,ids,steps]];r=m.reset_environment_batch(x,z,done,ids,steps)
 for row in range(len(x)):
  same(r['state'][row],z[row] if done[row] else x[row]);assert r['episode_ids'][row]==int(ids[row])+int(done[row]);assert r['steps'][row]==(0 if done[row] else steps[row])
 unchanged(before,[x,z,done,ids,steps]);assert all(not np.shares_memory(out,inp) for out in r.values() for inp in [x,z,done,ids,steps])
def invalid(m):
 base=[f([[1]]),f([[0]]),b([True]),i([1]),i([1])]
 for index,value in [(0,i([[1]])),(1,f([[np.nan]])),(2,i([1])),(3,i([-1])),(3,i([np.iinfo(np.int64).max])),(4,i([-1])),(4,i([]))]:
  a=base.copy();a[index]=value;reject(lambda:m.reset_environment_batch(*a))
 a=base.copy();a[1]=f([[np.inf]]);a[2]=b([False]);reject(lambda:m.reset_environment_batch(*a))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
