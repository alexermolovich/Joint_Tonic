import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):assert_array_equal(m.multimodal_causal_mask([0,1,2],[[True,False,True]]),[[[1,0,0],[0,0,0],[1,0,1]]])
def example2(m):assert_array_equal(m.multimodal_causal_mask([2],[[False],[True]]),[[[False]],[[True]]])
def invariants(m):
    p=np.array([[True]*4,[False]*4]);r=m.multimodal_causal_mask([2,0,1,2],p);assert r.dtype==bool;assert_array_equal(r[0],np.tril(np.ones((4,4),dtype=bool)));assert not r[1].any();assert p.all(axis=1).tolist()==[True,False]
    assert m.multimodal_causal_mask(np.array([],dtype=int),np.empty((2,0),dtype=bool)).shape==(2,0,0)
def invalid(m):
    for a in [([3],[[True]]),([-1],[[True]]),([0.],[[True]]),([0],[[1]]),([0],[[True,False]]),([0],np.empty((0,1),dtype=bool))]:bad(lambda:m.multimodal_causal_mask(*a))
TESTS=[('Missing sensor token','public',example1),('Batch-specific presence','public',example2),('Triangle, absent queries and empty sequence','hidden',invariants),('Invalid mask schema','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    p=np.ones((8,256),dtype=bool);p[:,1::2]=False;copy=p.copy();r=m.multimodal_causal_mask(np.arange(256)%3,p)
    assert r.shape==(8,256,256);assert not r[:,:,1::2].any() and not r[:,1::2,:].any();assert_array_equal(p,copy)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
