import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    v,a=m.sequence_masks([2,0],3); assert_array_equal(v,[[1,1,0],[0,0,0]])
    assert_array_equal(a[0],[[1,0,0],[1,1,0],[0,0,0]]); assert not a[1].any()
def one(m):
    v,a=m.sequence_masks([1],1); assert_array_equal(v,[[1]]); assert_array_equal(a,[[[1]]])
def empty(m):
    for lengths,T in [([],4),([0,0],0),([],0)]:
        v,a=m.sequence_masks(lengths,T); assert v.shape==(len(lengths),T) and a.shape==(len(lengths),T,T)
        assert v.dtype==bool and a.dtype==bool
def oracle(m):
    lengths=np.array([0,1,3,8]); old=lengths.copy(); v,a=m.sequence_masks(lengths,8)
    for b,L in enumerate(lengths):
        for i in range(8):
            assert v[b,i]==(i<L)
            for j in range(8): assert a[b,i,j]==(i<L and j<L and j<=i)
    assert_array_equal(lengths,old)
def invalid(m):
    for args in [([-1],3),([4],3),([.5],3),([True],3),([np.nan],3),([[1]],3),([1],True),([1],3.),([1],513),([0]*129,1)]:
        with np.testing.assert_raises(ValueError): m.sequence_masks(*args)
TESTS=[('Padding both axes','public',example),('Diagonal allowed','public',one),('Zero dimensions','hidden',empty),('Boolean predicate oracle','hidden',oracle),('Invalid mask contract','hidden',invalid)]
