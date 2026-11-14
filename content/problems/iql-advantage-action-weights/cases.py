import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def capped(m):assert_allclose(m.advantage_weights([[0,1,100]],[[0,0,0]],[[True,True,True]],1,2),[[1,2,2]])
def zero(m):assert_array_equal(m.advantage_weights([[4,7]],[[0,0]],[[True,False]],0,2),[[1,0]])
def scale(m):
    q=np.full((64,2048),1e6)[:,::2];v=-q;mask=np.ones_like(q,dtype=bool);r=m.advantage_weights(q,v,mask,100,1e6);assert_allclose(r,1e6);assert np.isfinite(r).all();assert not np.shares_memory(r,q);assert m.advantage_weights([[-1e6]],[[1e6]],[[True]],100,2)[0,0]==0

def invalid(m):
    for a in [([[1]],[[0]],[[True]],1,.5),([[1]],[[0]],[[True]],-1,2),([[1]],[[0]],[[1]],1,2)]:bad(lambda:m.advantage_weights(*a))
TESTS=[('Capped unnormalized weights','public',capped),('Zero inverse temperature','public',zero),('Scale overflow and underflow boundaries','hidden',scale),('Invalid weights','hidden',invalid)]
