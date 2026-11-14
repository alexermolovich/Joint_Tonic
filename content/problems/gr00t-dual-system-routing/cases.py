import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.route_dual_system([[5]],[[2]],[0],[[[3]]],[1],[1.2],.5);assert_array_equal(r['conditioning'],[[5,6]]);assert r['ready'][0];assert_allclose(r['context_age'],[.2])
def future(m):
    r=m.route_dual_system([[5]],[[2]],[0],[[[3]]],[2],[1],.5);assert not r['ready'][0] and r['context_age'][0]==-1

def scale(m):
    h=np.ones((64,128))[:,::2];s=h.copy();p=np.stack([np.eye(64),2*np.eye(64)]);ids=np.arange(64)%2;r=m.route_dual_system(h,s,ids,p,np.zeros(64),np.full(64,.5),.5);assert_array_equal(r['conditioning'][:,64:],np.repeat((ids+1)[:,None],64,axis=1));assert r['ready'].all();assert not np.shares_memory(r['conditioning'],h)
def invalid(m):
    for a in [([[1]],[[1]],[1],[[[1]]],[0],[0],0),([[1]],[[1]],[0],[[[1]]],[-1],[0],0),([[1]],[[1]],[0.],[[[1]]],[0],[0],0)]:bad(lambda:m.route_dual_system(*a))
TESTS=[('Embodiment-specific conditioning','public',one),('Future semantic context','public',future),('Scale and inclusive age limit','hidden',scale),('Invalid routing','hidden',invalid)]
