import numpy as np
from numpy.testing import assert_array_equal


def best(m):
    masks=np.array([[[1,0]],[[0,1]],[[1,1]]],dtype=bool)
    selected,indices,scores=m.rank_masks(masks,np.array([.7,.9,.8]),2)
    assert_array_equal(selected,[[[0,1]],[[1,1]]]);assert_array_equal(indices,[1,2]);assert_array_equal(scores,[.9,.8])


def raw_ties(m):
    selected,indices,scores=m.rank_masks(np.array([[[1]],[[0]],[[1]]],dtype=bool),np.array([1.2,1.2,-.1]),2)
    assert_array_equal(indices,[0,1]);assert_array_equal(scores,[1.2,1.2]);assert_array_equal(selected,[[[1]],[[0]]])


def empty(m):
    a,b,c=m.rank_masks(np.empty((0,2,3),dtype=bool),np.empty(0),0)
    assert a.shape==(0,2,3) and b.shape==c.shape==(0,)
    assert a.dtype==np.bool_ and b.dtype==np.int64 and c.dtype==np.float64


def no_selection(m):
    a,b,c=m.rank_masks(np.ones((5,3,4),dtype=bool),np.arange(5,dtype=float),0)
    assert a.shape==(0,3,4) and b.size==c.size==0


def oracle_storage(m):
    rng=np.random.default_rng(20261113)
    masks=(rng.random((27,5,7))>.5)[:,:,::-1]
    scores=rng.integers(-4,5,27).astype(float);oldm=masks.copy();olds=scores.copy()
    a,b,c=m.rank_masks(masks,scores,11)
    expected=sorted(range(27),key=lambda i:(-scores[i],i))[:11]
    assert_array_equal(b,expected);assert_array_equal(a,masks[expected]);assert_array_equal(c,scores[expected])
    assert not np.shares_memory(a,masks) and not np.shares_memory(c,scores)
    assert_array_equal(masks,oldm);assert_array_equal(scores,olds)


def invalid(m):
    with np.testing.assert_raises(TypeError):m.rank_masks([],np.empty(0),0)
    for masks,s,k in [(np.ones((1,2,2)),np.ones(1),1),(np.ones((1,2,2),dtype=bool),np.ones(1,dtype=np.float32),1),(np.ones((1,2,2),dtype=bool),np.ones(2),1),(np.ones((1,2,2),dtype=bool),np.array([np.nan]),1),(np.ones((1,2,2),dtype=bool),np.ones(1),True),(np.ones((1,2,2),dtype=bool),np.ones(1),2),(np.empty((0,0,2),dtype=bool),np.empty(0),0)]:
        with np.testing.assert_raises(ValueError):m.rank_masks(masks,s,k)


TESTS=[("Best mask interpretations","public",best),("Stable raw score ties","public",raw_ties),("Empty candidates","public",empty),
       ("Zero selections","hidden",no_selection),("Independent stable ranking oracle","hidden",oracle_storage),("Validation","hidden",invalid)]
