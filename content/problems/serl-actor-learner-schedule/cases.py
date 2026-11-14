import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.schedule_learner([2,0,1],0,2,1,3,2);assert_array_equal(r['updates'],[3,1,2]);assert_array_equal(r['completed'],[3,4,6]);assert_array_equal(r['backlog'],[1,0,0]);assert_array_equal(r['published_version'],[3,4,6]);assert r['publish'].all()
def warmup(m):
    r=m.schedule_learner([2,1],2,1,2,10,2);assert not r['updates'].any() and not r['publish'].any()
def accounting(m):
    new=np.full(8192,10000,np.int64)[::2];r=m.schedule_learner(new,100,32,3,1000,333);expected=np.minimum(np.arange(1,4097,dtype=np.int64)*1000,((np.cumsum(new)-100)*32)//3);assert_array_equal(r['completed'],expected);assert_array_equal(r['backlog'],((np.cumsum(new)-100)*32)//3-expected);assert r['backlog'][-1]>100000000;assert not np.shares_memory(r['updates'],new)
    r=m.schedule_learner([1,1,1,0],0,1,1,1,2);assert_array_equal(r['published_version'],[0,2,2,2]);assert_array_equal(r['publish'],[False,True,False,False])
    r=m.schedule_learner(np.empty(0,int),0,1,1,1,1);assert r['updates'].shape==(0,)
def invalid(m):
    for args in [([1],True,1,1,1,1),([1],0,1,0,1,1),([10001],0,1,1,1,1),([1],0,1,1,10**1000,1),([1.],0,1,1,1,1)]:bad(lambda:m.schedule_learner(*args))
TESTS=[('Backlog and publication crossings','public',one),('Warmup and exact fractional ratio','public',warmup),('Exact integer budget at scale sparse publication and empty input','hidden',accounting),('Invalid schedule counters','hidden',invalid)]
