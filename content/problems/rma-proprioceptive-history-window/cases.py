import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def past(m):
    r=m.window_history([[1],[2],[3]],[[.1],[.2],[.3]],[0,0,0],[2],3);assert_allclose(r['history'],[[[0,0],[1,.1],[2,.2]]]);assert_array_equal(r['source_indices'],[[-1,0,1]])
def boundary(m):
    r=m.window_history([[1],[2],[3]],[[.1],[.2],[.3]],[0,0,1],[2],3);assert not r['valid'].any();assert not r['history'].any()
def scale(m):
    o=np.ones((4096,64))[:,::2];a=o*2;ep=np.arange(4096)//32;q=np.arange(0,4096,32);r=m.window_history(o,a,ep,q,64);assert r['history'].shape==(128,64,64);assert not r['valid'].any();assert not np.shares_memory(r['history'],o)
    r=m.window_history([[1],[2],[3]],[[10],[20],[30]],[0,0,0],[2,0],1);assert_array_equal(r['history'],[[[2,20]],[[0,0]]]);assert_array_equal(r['source_indices'],[[1],[-1]])
    assert m.window_history([[0]],[[0]],[0],np.empty(0,int),1)['history'].shape==(0,1,2)
def invalid(m):
    for a in [([[0],[0]],[[0],[0]],[1,0],[1],1),([[0]],[[0]],[0],[1],1),([[0]],[[0]],[0],[0],True),([[0]],[[np.nan]],[0],[0],1)]:bad(lambda:m.window_history(*a))
TESTS=[('Past-only padded history','public',past),('Episode reset','public',boundary),('Scale current-action exclusion and empty queries','hidden',scale),('Invalid records','hidden',invalid)]
