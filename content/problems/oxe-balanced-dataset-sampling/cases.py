import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    g,i=m.sample_dataset_mixture([2,4],[1,3],[[0,.9],[.25,.5]]);assert_array_equal(g,[0,1]);assert_array_equal(i,[1,2])
def example2(m):
    g,i=m.sample_dataset_mixture([3,2,5],[0,1,0],[[0,0],[.99,.99]]);assert_array_equal(g,[1,1]);assert_array_equal(i,[0,1])
def scale_empty(m):
    u=np.column_stack((np.arange(10000)/10000,np.full(10000,.5)));g,i=m.sample_dataset_mixture([2,8],[1,1],u);assert np.bincount(g).tolist()==[5000,5000];assert_array_equal(i[:5000],np.ones(5000));assert_array_equal(i[5000:],np.full(5000,4));assert g.dtype==np.int64
    g,i=m.sample_dataset_mixture([1],[1],np.empty((0,2)));assert g.shape==i.shape==(0,)
def invalid(m):
    for a in [([0],[1],[[0,0]]),([1],[0],[[0,0]]),([1],[-1],[[0,0]]),([1],[1],[[1,0]]),([1],[1],[[0,np.nan]]),([1.],[1],[[0,0]]),([1],[1,2],[[0,0]])]:bad(lambda:m.sample_dataset_mixture(*a))
TESTS=[('Weighted CDF boundary','public',example1),('Zero-weight sources','public',example2),('Deterministic mixture scale and empty batch','hidden',scale_empty),('Invalid sampling contract','hidden',invalid)]

def tiny_tail(m):
    g,i=m.sample_dataset_mixture([1]*7,[1,1,1,1,1,1,0],[[np.nextafter(1.,0.),0]]);assert_array_equal(g,[5])
TESTS.append(("Trailing zero-weight roundoff", "hidden", tiny_tail))
