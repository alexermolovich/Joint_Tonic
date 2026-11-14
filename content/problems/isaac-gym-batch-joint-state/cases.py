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

def example1(m):same(m.batch_joint_states(f([[1,10],[2,20],[3,30],[4,40]]),i([[2,0],[3,1]])),[[[3,30],[1,10]],[[4,40],[2,20]]])
def example2(m):assert m.batch_joint_states(np.zeros((0,2)),np.zeros((0,3),dtype=np.int64)).shape==(0,3,2)
def edges(m):
 x=np.array([[1,2],[3,4],[5,6]],dtype=np.float32);r=m.batch_joint_states(x,i([[2]]));same(r,[[[5,6]]]);assert r.dtype==np.float64 and not np.shares_memory(x,r)
 reject(lambda:m.batch_joint_states(x,i([[1],[1]])))
def oracle_scale(m):
 rng=np.random.default_rng(926);x=rng.normal(size=(100000,4))[:,::2];idx=rng.permutation(100000)[:65536].reshape(512,128)[:,::2];before=[x.copy(),idx.copy()];r=m.batch_joint_states(x,idx)
 for row in range(len(idx)):same(r[row],[[float(x[j,0]),float(x[j,1])] for j in idx[row]])
 unchanged(before,[x,idx]);assert not np.shares_memory(r,x)
def invalid(m):
 for x,idx in [(f([[1,2]]),i([[-1]])),(f([[1,2]]),i([[1]])),(f([[1,2]]),f([[0]])),(f([[1,2,3]]),i([[0]])),(f([[1,2],[np.nan,0]]),i([[0]])),(f([[1,2]]),np.zeros((0,0),dtype=np.int64)),(f([[1,2]]),np.zeros((0,257),dtype=np.int64))]:reject(lambda:m.batch_joint_states(x,idx))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
