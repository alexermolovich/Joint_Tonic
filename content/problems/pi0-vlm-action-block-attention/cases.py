import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):assert_array_equal(m.vlm_action_mask([[True]],[[True,True]]),[[[1,0,0],[1,1,1],[1,1,1]]])
def missing(m):
    r=m.vlm_action_mask([[False]],[[True,False]]);assert r.sum()==1 and r[0,1,1]
def scale(m):
    c=np.ones((16,256),bool)[:,::2];a=c.copy();a[:,1]=False;r=m.vlm_action_mask(c,a);assert r.shape==(16,256,256);assert not r[:,:128,128:].any();assert not r[:,129,:].any();assert not r[:,:,129].any();assert m.vlm_action_mask(np.empty((1,0),bool),[[True]])[0,0,0]
def invalid(m):
    for a in [([[1]],[[True]]),([[True]],[[True],[False]]),([[True]],np.empty((1,0),bool))]:bad(lambda:m.vlm_action_mask(*a))
TESTS=[('Asymmetric context/action blocks','public',one),('Missing tokens','public',missing),('Scale strided masks and no context','hidden',scale),('Invalid blocks','hidden',invalid)]
