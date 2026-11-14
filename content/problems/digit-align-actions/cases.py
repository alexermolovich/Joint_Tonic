import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def causal(m):
    r=m.align_tactile_actions([.5,1],[0,1],[[.2],[.8]],.5);assert_array_equal(r['indices'],[0,1]);assert_allclose(r['age'],[.5,0]);assert r['valid'].all();assert_allclose(r['aligned'],[[.2],[.8]])
def stale(m):
    r=m.align_tactile_actions([.5,2],[1],[[.8]],.5);assert_array_equal(r['indices'],[-1,0]);assert_allclose(r['age'],[np.nan,1]);assert not r['valid'].any();assert not r['aligned'].any()
def scale(m):
    t=np.arange(4096,dtype=float);a=np.zeros((4096,32))[:,::2];a[:,0]=np.linspace(-1,1,4096);r=m.align_tactile_actions(t[::-1],t,a,0);assert_array_equal(r['indices'],np.arange(4096)[::-1]);assert_array_equal(r['aligned'],a[::-1]);assert not np.shares_memory(r['aligned'],a)
    r=m.align_tactile_actions([0,1],[],np.empty((0,3)),0);assert_array_equal(r['indices'],[-1,-1]);assert np.isnan(r['age']).all();assert r['aligned'].shape==(2,3)
    r=m.align_tactile_actions([],[],np.empty((0,3)),0);assert r['aligned'].shape==(0,3)
def invalid(m):
    for a in [([1],[1,1],[[0],[0]],1),([0],[1],[[np.nan]],1),([0],[1],[[2]],1)]:bad(lambda:m.align_tactile_actions(*a))
TESTS=[('Causal hold and exact timestamp','public',causal),('Future and stale commands','public',stale),('Scale unsorted frames and empty commands','hidden',scale),('Invalid command records','hidden',invalid)]
