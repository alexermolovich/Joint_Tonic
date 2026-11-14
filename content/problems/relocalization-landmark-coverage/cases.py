import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def duplicate(m):
 r=m.relocalization_coverage(np.array([[0.,0.],[3.,3.]]),np.array([[7,7]]),np.ones((1,2),bool),np.array([4,4]),np.array([2,2]),2,2);assert_array_equal(r['unique_landmarks'],[1]);assert_array_equal(r['covered_cells'],[1]);assert r['best']==-1
def distinct(m):
 r=m.relocalization_coverage(np.array([[0.,0.],[3.,3.]]),np.array([[7,8]]),np.ones((1,2),bool),np.array([4,4]),np.array([2,2]),2,2);assert_array_equal(r['unique_landmarks'],[2]);assert_array_equal(r['covered_cells'],[2]);assert r['best']==0
def oracle(m):
 rng=np.random.default_rng(848);uv=rng.uniform(0,63,(2048,4))[:,::2];ids=rng.integers(-1,700,(32,4096),dtype=np.int64)[:,::2];mask=(rng.random(ids.shape)>.2)&(ids>=0);before=ids.copy();r=m.relocalization_coverage(uv,ids,mask,np.array([64,64]),np.array([4,8]),100,20);counts=[];coverage=[]
 for row in range(32):
  seen=set();cells=set()
  for i in range(2048):
   if mask[row,i] and int(ids[row,i]) not in seen:seen.add(int(ids[row,i]));cells.add((int(uv[i,1]*4/64),int(uv[i,0]*8/64)))
  counts.append(len(seen));coverage.append(len(cells))
 expected=[i for i in range(32) if counts[i]>=100 and coverage[i]>=20];expected.sort(key=lambda i:(-counts[i],-coverage[i],i));assert_array_equal(r['unique_landmarks'],counts);assert_array_equal(r['covered_cells'],coverage);assert_array_equal(r['order'],expected);assert_array_equal(ids,before);assert not np.shares_memory(r['unique_landmarks'],ids)
def edges(m):
 r=m.relocalization_coverage(np.empty((0,2)),np.empty((2,0),np.int64),np.empty((2,0),bool),np.array([1,1]),np.array([1,1]),1,1);assert r['best']==-1
 r=m.relocalization_coverage(np.array([[0.,0.],[2.,2.]]),np.array([[1,2],[1,2]]),np.ones((2,2),bool),np.array([4,4]),np.array([2,2]),2,2);assert_array_equal(r['covered_cells'],[2,2]);assert_array_equal(r['order'],[0,1])
def invalid(m):
 def call(ids,mask,n):return m.relocalization_coverage(np.zeros((1,2)),ids,mask,np.array([2,2]),np.array([1,1]),n,1)
 bad(lambda:call(np.array([[-1]]),np.ones((1,1),bool),1));bad(lambda:call(np.array([[1]]),np.ones((1,1),bool),10**1000));bad(lambda:call(np.array([[1]]),np.ones((1,1),bool),True));bad(lambda:call(np.array([[1.]]),np.ones((1,1),bool),1))
TESTS=[('Duplicate identities do not inflate coverage','public',duplicate),('Distinct geometric support','public',distinct),('Independent identity-set and grid oracle at scale','hidden',oracle),('No evidence boundaries and stable ties','hidden',edges),('Invalid landmark masks and count thresholds','hidden',invalid)]
