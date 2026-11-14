import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def tie(m):
    r=m.offline_action_support([0,0],[[0],[1]],[0],[[.5]],.5);assert_array_equal(r['nearest_index'],[0]);assert_allclose(r['distance'],[.5]);assert not r['unsupported'][0]
def unknown(m):
    r=m.offline_action_support([0],[[0]],[1],[[0]],1);assert r['nearest_index'][0]==-1 and np.isnan(r['distance'][0]) and r['unsupported'][0]
def scale(m):
    s=np.arange(1024,dtype=np.int64);a=np.zeros((1024,32))[:,::2];q=s[::4];u=np.zeros((256,16));r=m.offline_action_support(s,a,q,u,0);assert_array_equal(r['nearest_index'],q);assert not r['unsupported'].any();assert not np.shares_memory(r['nearest_index'],s)
    r=m.offline_action_support(np.empty(0,dtype=int),np.empty((0,2)),[0],[[0,0]],1);assert r['unsupported'][0]
    r=m.offline_action_support([0],[[0]],np.empty(0,dtype=int),np.empty((0,1)),0);assert r['distance'].shape==(0,)
def invalid(m):
    for args in [([0],[[2]],[0],[[0]],1),([0.],[[0]],[0],[[0]],1),([0],[[0]],[-1],[[0]],1)]:bad(lambda:m.offline_action_support(*args))
TESTS=[('Equal distance tie','public',tie),('Missing state support','public',unknown),('Scale and empty sets','hidden',scale),('Invalid inputs','hidden',invalid)]
