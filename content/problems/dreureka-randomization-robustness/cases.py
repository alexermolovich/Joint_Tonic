import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.randomization_robustness([[True,False],[False,False]],[[True]*2]*2,0,2);assert_allclose(r['success_rate'],[.5,0]);assert_allclose(r['paired_delta'],[0,-.5]);assert r['worst_index']==1

def missing(m):
    r=m.randomization_robustness([[True,False],[False,False]],[[True,True],[False,True]],0,2);assert_allclose(r['paired_delta'],[0,0]);assert_array_equal(r['paired_counts'],[2,1]);assert r['worst_index']==0

def oracle(m):
    rng=np.random.default_rng(538);s=rng.random((128,8192))[:,::2]>.5;v=rng.random(s.shape)>.2;before=s.copy();r=m.randomization_robustness(s,v,3,1)
    for g in range(128):
        paired=[j for j in range(4096) if v[g,j] and v[3,j]];expected=sum(int(s[g,j])-int(s[3,j]) for j in paired)/len(paired);assert_allclose(r['paired_delta'][g],expected)
    assert_array_equal(s,before);assert not np.shares_memory(r['counts'],v)
    r=m.randomization_robustness([[True],[False]],[[False],[True]],0,1);assert r['worst_index']==-1 and np.isnan(r['paired_delta']).all()
    r=m.randomization_robustness(np.empty((1,0),bool),np.empty((1,0),bool),0,1);assert r['worst_index']==-1

def invalid(m):
    bad(lambda:m.randomization_robustness([[True]],[[True]],True,1));bad(lambda:m.randomization_robustness([[1]],[[True]],0,1));bad(lambda:m.randomization_robustness([[True]],[[True]],0,10**1000))
TESTS=[('Paired degradation','public',one),('Missing paired seeds','public',missing),('Independent paired oracle and scale','hidden',oracle),('Invalid comparison','hidden',invalid)]
