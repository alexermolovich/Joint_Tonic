import numpy as np
from numpy.testing import assert_array_equal
def example(m):
    f,b=m.detector_frontier(np.array([.7,.8,.75]),np.array([10.,20,25]),20);assert_array_equal(f,[0,1]);assert b==1
def duplicates(m):
    f,b=m.detector_frontier(np.array([.8,.8]),np.array([20.,20]),19);assert_array_equal(f,[0,1]);assert b==-1
def ties(m):
    f,b=m.detector_frontier(np.array([.5,.5,.5]),np.array([3.,2,2]),2);assert_array_equal(f,[1,2]);assert b==1
    f,b=m.detector_frontier(np.empty(0),np.empty(0),1);assert f.dtype==np.int64 and f.shape==(0,) and b==-1
def oracle(m):
    r=np.random.default_rng(22);a=r.uniform(0,1,77);l=r.uniform(1,100,77);ac=a.copy();lc=l.copy();f,b=m.detector_frontier(a,l,40)
    expected=[i for i in range(77) if not any(a[j]>=a[i] and l[j]<=l[i] and (a[j]>a[i] or l[j]<l[i]) for j in range(77))]
    assert_array_equal(f,expected);assert b==min([i for i in range(77) if l[i]<=40],key=lambda i:(-a[i],l[i],i));assert_array_equal(a,ac);assert_array_equal(l,lc)
def invalid(m):
    for a,l,b in [(np.array([1.1]),np.ones(1),1),(np.ones(1),np.zeros(1),1),(np.ones(2),np.ones(1),1),(np.ones(1),np.ones(1),True),(np.ones(1),np.ones(1),np.nan)]:
        with np.testing.assert_raises(ValueError):m.detector_frontier(a,l,b)
TESTS=[('Dominated detector','public',example),('Duplicates and infeasibility','public',duplicates),('Tie rules and empty benchmark','hidden',ties),('Pairwise scalar oracle','hidden',oracle),('Validation','hidden',invalid)]
