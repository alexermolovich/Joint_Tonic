import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def stable(m):
    r=m.recovery_metrics([0,1,2,3],[[2,.2,.1,.1]],[[True]*4],1,.1,2);assert r['recovered'][0] and r['index'][0]==2;assert r['delay'][0]==1;assert_allclose(r['post_change_mean'],[.4/3]);assert_array_equal(r['counts'],[3])
def gap(m):
    r=m.recovery_metrics([0,1,2,3],[[2,.2,.1,.1]],[[True,True,False,True]],1,.1,2);assert not r['recovered'][0] and r['index'][0]==-1 and np.isnan(r['delay'][0])
def scale(m):
    t=np.arange(4096,dtype=float)+1000;e=np.ones((128,8192))[:,::2]*1000;mask=np.ones_like(e,bool);r=m.recovery_metrics(t,e,mask,2000,1000,64);assert_array_equal(r['index'],np.full(128,2000));assert_array_equal(r['delay'],np.zeros(128));assert_allclose(r['post_change_mean'],1000);assert not np.shares_memory(r['index'],e)
    assert not m.recovery_metrics([0,1],[[0,0]],[[True,True]],1,0,2)['recovered'][0]
    r=m.recovery_metrics([0],[[1]],[[False]],0,0,1);assert np.isnan(r['post_change_mean'][0]) and r['counts'][0]==0
def invalid(m):
    for a in [([0,0],[[1,1]],[[True,True]],0,1,1),([0],[[1]],[[True]],True,1,1),([0],[[np.nan]],[[False]],0,1,1),([0],[[1]],[[True]],0,1,2)]:bad(lambda:m.recovery_metrics(*a))
TESTS=[('Stable post-change window','public',stable),('Missing evidence breaks recovery','public',gap),('Scale boundaries and absent traces','hidden',scale),('Invalid recovery contract','hidden',invalid)]
