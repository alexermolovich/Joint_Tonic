import numpy as np
from numpy.testing import assert_array_equal,assert_allclose
def example(m):
    i,s=m.select_grounded_queries(np.array([[1.,100,3],[4,0,2],[4,9,1]]),np.array([True,False,True]),2);assert_array_equal(i,[1,2]);assert_allclose(s,[4,4])
def negatives(m):
    i,s=m.select_grounded_queries(np.array([[-3.,-1],[-2,-4]]),np.ones(2,bool),1);assert_array_equal(i,[0]);assert_allclose(s,[-1])
def oracle(m):
    r=np.random.default_rng(81);a=r.integers(-3,4,(101,17)).astype(float);mask=np.arange(17)%3==0;i,s=m.select_grounded_queries(a,mask,37);ranks=[max(row[mask]) for row in a];order=sorted(range(101),key=lambda q:(-ranks[q],q))[:37];assert_array_equal(i,order);assert_allclose(s,[ranks[q] for q in order])
def zero(m):
    i,s=m.select_grounded_queries(np.empty((0,3)),np.zeros(3,bool),0);assert i.shape==s.shape==(0,) and i.dtype==np.int64 and s.dtype==np.float64
def invalid(m):
    for a,v,k in [(np.ones((1,2)),np.zeros(2,bool),1),(np.ones((1,2)),np.ones(2,bool),True),(np.ones((1,2)),np.ones(2,bool),2),(np.ones((1,2)),np.ones(1,bool),1)]:
        with np.testing.assert_raises(ValueError):m.select_grounded_queries(a,v,k)
TESTS=[('Masked maxima and tie order','public',example),('Negative logits','public',negatives),('Independent sorting oracle','hidden',oracle),('Zero queries','hidden',zero),('Validation','hidden',invalid)]

def scale_storage(m):
    base=np.arange(4096*8,dtype=np.float64).reshape(4096,8);scores=base[:,::2];mask=np.array([True,False,True,False]);before=scores.copy();idx,rank=m.select_grounded_queries(scores,mask,32)
    assert_array_equal(idx,np.arange(4095,4063,-1));assert_allclose(rank,scores[idx,2]);assert_array_equal(scores,before)
    for a in (idx,rank):assert not np.shares_memory(a,scores)

TESTS.append(('Scale noncontiguous and noalias','hidden',scale_storage))
