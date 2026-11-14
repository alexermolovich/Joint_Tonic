import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.sensor_readiness([[True,True]],[[9,8]],[10],[1,1],[True,True]);assert_array_equal(r['usable'],[[True,False]]);assert_array_equal(r['stale'],[[False,True]]);assert_array_equal(r['ready'],[False])
def example2(m):
    r=m.sensor_readiness([[False,True]],[[0,11]],[10],[1,1],[False,False]);assert_array_equal(r['usable'],[[False,False]]);assert_array_equal(r['stale'],[[False,True]]);assert_array_equal(r['ready'],[True])
def batch(m):
    r=m.sensor_readiness([[True],[False]],[[3],[3]],[3,3],[0],[True]);assert_array_equal(r['ready'],[True,False]);assert not r['stale'].any()
def invalid(m):
    good=[[[True]],[[0]],[1],[1],[True]]
    for i,v in [(0,[[1]]),(1,[[np.nan]]),(1,[[-1]]),(2,[1,2]),(3,[-1]),(4,[1])]:
        a=good.copy();a[i]=v;bad(lambda:m.sensor_readiness(*a))
TESTS=[('Freshness boundary','public',example1),('Future stamp and optional sensors','public',example2),('Batch and missing required sensor','hidden',batch),('Invalid sensor metadata','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    p=np.ones((64,32),dtype=bool);s=np.ones((64,64))[:,::2];copy=s.copy();r=m.sensor_readiness(p,s,np.full(64,2.),np.ones(32),np.ones(32,dtype=bool));assert r['ready'].all();assert r['usable'].all();assert not r['stale'].any();assert_array_equal(s,copy)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
