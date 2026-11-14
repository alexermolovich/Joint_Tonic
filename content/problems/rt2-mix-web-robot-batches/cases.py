import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.mix_web_robot([2],[8,9],.5,5);assert_array_equal(r['source'],[1,1,1,0,0]);assert_array_equal(r['ids'],[8,9,8,2,2])
def example2(m):
    r=m.mix_web_robot([4,5],np.array([],dtype=int),0,3);assert_array_equal(r['source'],[0,0,0]);assert_array_equal(r['ids'],[4,5,4])
def extremes(m):
    r=m.mix_web_robot(np.array([],dtype=int),[7],1,4);assert_array_equal(r['ids'],[7]*4);assert r['source'].dtype==np.int64
    assert_array_equal(m.mix_web_robot([0],[1],.5,1)['source'],[1])
def invalid(m):
    for a in [([0],np.array([],dtype=int),1,2),([-1],[2],.5,2),([0.],[2],.5,2),([0],[2],1.1,2),([0],[2],.5,0),([0],[2],.5,True),([0],[2],.5,10**1000)]:bad(lambda:m.mix_web_robot(*a))
TESTS=[('Half-up source quotas','public',example1),('Unused empty source','public',example2),('Extreme ratios','hidden',extremes),('Invalid mixer inputs','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    w=np.arange(20000,dtype=np.int64)[::2];r=np.arange(100,dtype=np.int64);c=w.copy();out=m.mix_web_robot(w,r,.25,4096)
    assert out['source'].sum()==1024 and out['ids'].shape==(4096,);assert_array_equal(out['ids'][:1024],np.arange(1024)%100);assert_array_equal(w,c);assert not np.shares_memory(out['ids'],w)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
