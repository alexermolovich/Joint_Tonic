"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):
    np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)

def run(m,g,n):return m.aggregate_learner_gradients(np.array(g,dtype=np.float64),np.array(n,dtype=np.int64))
def example1(m):
 r=run(m,[[1],[3]],[2,6]);same(r['mean'],[2.5]);assert r['norm']==2.5 and r['total_samples']==8 and r['has_samples'] is True

def example2(m):
 r=run(m,[[100,-20]],[0]);same(r['mean'],[0,0]);assert r['norm']==0 and r['total_samples']==0 and r['has_samples'] is False

def edges(m):
 r=m.aggregate_learner_gradients(np.zeros((0,2),dtype=np.float32),np.zeros(0,dtype=np.int64));same(r['mean'],[0,0]);assert r['mean'].dtype==np.float64
 r=m.aggregate_learner_gradients(np.array([[3,4]],dtype=np.float32),np.array([1000000],dtype=np.int64));assert r['norm']==5 and r['total_samples']==1000000

def oracle_scale(m):
 rng=np.random.default_rng(913);g=rng.normal(size=(4096,128))[:,::2];n=np.arange(4096,dtype=np.int64)%17;before=[g.copy(),n.copy()];r=m.aggregate_learner_gradients(g,n);total=sum(int(v) for v in n)
 expected=[sum(float(g[i,j])*int(n[i]) for i in range(4096))/total for j in range(64)];same(r['mean'],expected);same(r['norm'],sum(v*v for v in expected)**.5);assert r['total_samples']==total
 for a,b in zip(before,[g,n]):np.testing.assert_array_equal(a,b)
 assert not np.shares_memory(r['mean'],g)
def invalid(m):
 for g,n in [([[float('nan')]],[0]),([[1]],[-1]),([[1]],[]),([[1]],[10**6+1]),([[1e7]],[1])]:reject(lambda:run(m,g,n))
 reject(lambda:m.aggregate_learner_gradients(np.ones((1,1),dtype=np.int64),np.array([1],dtype=np.int64)));reject(lambda:m.aggregate_learner_gradients(np.zeros((1,0)),np.array([1],dtype=np.int64)))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
