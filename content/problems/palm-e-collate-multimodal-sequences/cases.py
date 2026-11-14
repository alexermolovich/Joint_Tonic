import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.collate_multimodal([[[1],[2]],[[3]]],[[0,2],[1]]);assert_array_equal(r['tokens'],[[[1],[2]],[[3],[0]]]);assert_array_equal(r['modalities'],[[0,2],[1,-1]]);assert_array_equal(r['present'],[[True,True],[True,False]]);assert_array_equal(r['lengths'],[2,1])
def example2(m):
    r=m.collate_multimodal([np.empty((0,2)),[[0,0]]],[np.array([],dtype=int),[2]]);assert_array_equal(r['tokens'],np.zeros((2,1,2)));assert_array_equal(r['present'],[[False],[True]])
def empty_storage(m):
    r=m.collate_multimodal([np.empty((0,3))],[np.array([],dtype=int)]);assert r['tokens'].shape==(1,0,3)
    x=np.arange(12.).reshape(3,4)[:,::2];copy=x.copy();r=m.collate_multimodal([x],[[0,1,2]]);assert_array_equal(r['tokens'][0],x);assert_array_equal(x,copy);assert not np.shares_memory(x,r['tokens'])
def invalid(m):
    for a in [([],[]),([[[1]]],[]),([[[1]],[[2,3]]],[[0],[1]]),([[[1]]],[[3]]),([[[1]]],[[0.]]),([[[np.nan]]],[[0]])]:bad(lambda:m.collate_multimodal(*a))
TESTS=[('Right padding','public',example1),('Real zero token versus padding','public',example2),('All empty and storage','hidden',empty_storage),('Invalid multimodal batch','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    xs=[np.full((i*8,16),float(i)) for i in range(1,17)];ms=[np.arange(len(x))%3 for x in xs];r=m.collate_multimodal(xs,ms)
    assert r['tokens'].shape==(16,128,16);assert_array_equal(r['lengths'],np.arange(1,17)*8)
    for i,x in enumerate(xs):assert_array_equal(r['tokens'][i,:len(x)],x);assert not r['present'][i,len(x):].any()

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
