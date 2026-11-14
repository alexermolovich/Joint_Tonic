import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.heterogeneous_batch([[1],[2]],[[[0],[2]],None],[0,1],[3,-1]);assert_array_equal(r['actions'],[[[0],[2]],[[0],[0]]]);assert_array_equal(r['action_mask'],[[[1],[1]],[[0],[0]]])
def video(m):assert m.heterogeneous_batch([[5]],[None],[1],[-1])['actions'].shape==(1,0,0)
def scale(m):
    x=np.ones((32,256))[:,::2];a=np.ones((64,64))[:,::2];r=m.heterogeneous_batch(x,[a]*32,np.arange(32)%2*2,np.arange(32)%16);assert r['actions'].shape==(32,64,32) and r['action_mask'].all();assert not np.shares_memory(r['observations'],x)
    r=m.heterogeneous_batch([[0],[0]],[[[0,1]],[[2],[3]]],[0,2],[0,1]);assert_array_equal(r['action_mask'],[[[1,1],[0,0]],[[1,0],[1,0]]])
def invalid(m):
    for a in [([[1]],[[[1]]],[1],[-1]),([[1]],[None],[0],[0]),([[1]],[None],[1],[0]),([[1]],[[[1]]],[2],[16])]:bad(lambda:m.heterogeneous_batch(*a))
TESTS=[('Robot and video masks','public',one),('Video-only batch','public',video),('Scale and mixed shape padding','hidden',scale),('Invalid source/label combinations','hidden',invalid)]
