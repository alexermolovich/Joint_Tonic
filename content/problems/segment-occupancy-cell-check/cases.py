import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def fixture():
    grid=np.zeros((3,3)); grid[1,1]=1; return grid
def crossing(m):
    assert m.segment_is_free(fixture(),[0,1.5],[3,1.5]) is False
def clear(m):
    assert m.segment_is_free(fixture(),[0,0],[3,0]) is True
def grazing(m):
    g=fixture(); assert not m.segment_is_free(g,[0,0],[1,1]); assert not m.segment_is_free(g,[0,1],[3,1])
    assert m.segment_is_free(g,[0,0],[.999,.999]); assert not m.segment_is_free(g,[1.5,1.5],[1.5,1.5]); assert m.segment_is_free(g,[0,0],[0,0])
def reversal(m):
    g=fixture(); old=g.copy()
    for a,b in [([0,2.5],[3,.2]),([0,.2],[3,.2]),([3,3],[2,2]),([0,3],[3,0])]: assert m.segment_is_free(g,a,b)==m.segment_is_free(g,b,a)
    assert_array_equal(g,old); assert m.segment_is_free(np.zeros((128,128)),[0,0],[128,128])
def invalid(m):
    for g,a,b in [([[2]],[0,0],[1,1]),([[0]],[-1,0],[1,1]),([[0]],[0,0],[2,0]),([[True]],[0,0],[1,1]),([[0]],[0,np.nan],[1,1])]:
        with np.testing.assert_raises(ValueError): m.segment_is_free(g,a,b)
TESTS=[('Continuous crossing','public',crossing),('Clear segment','public',clear),('Corner edge and zero-length contact','hidden',grazing),('Reversal and preservation','hidden',reversal),('Invalid map inputs','hidden',invalid)]
