import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    y,g=m.interleave_modal_tokens([[1,2]],[[3,4]],[[5,6]],[[2,0],[0,0],[1,0]]);assert_array_equal(y,[[5,6],[1,2],[3,4]]);assert_array_equal(g,[2,0,1])
def example2(m):
    y,g=m.interleave_modal_tokens([[7]],np.empty((0,1)),np.empty((0,1)),[[0,0],[0,0]]);assert_array_equal(y,[[7],[7]]);assert_array_equal(g,[0,0])
def storage_empty(m):
    x=np.arange(8.).reshape(2,4)[:,::2];c=x.copy();y,g=m.interleave_modal_tokens(x,x,x,[[0,1],[2,0]]);assert_array_equal(y,[x[1],x[0]]);assert not np.shares_memory(y,x);assert_array_equal(x,c)
    y,g=m.interleave_modal_tokens(x,x,x,np.empty((0,2),dtype=int));assert y.shape==(0,2) and g.shape==(0,) and g.dtype==np.int64
def invalid(m):
    for a in [([[1]],[[2,3]],[[4]],[[0,0]]),([[1]],[[2]],[[3]],[[3,0]]),([[1]],[[2]],[[3]],[[0,1]]),([[1]],[[2]],[[3]],[[-1,0]]),([[1]],[[2]],[[3]],[[0.,0.]]),([[np.nan]],[[2]],[[3]],np.empty((0,2),dtype=int))]:bad(lambda:m.interleave_modal_tokens(*a))
TESTS=[('Prompt order','public',example1),('Repeated source token','public',example2),('Empty sequence and independent storage','hidden',storage_empty),('Invalid source references','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    x=np.arange(512*4,dtype=float).reshape(512,4)[:,::2];order=np.column_stack((np.arange(1024)%3,np.arange(1024)%512));copy=x.copy();y,g=m.interleave_modal_tokens(x,x+1,x+2,order)
    for k in [0,1,511,1023]:assert_array_equal(y[k],x[k%512]+k%3)
    assert_array_equal(x,copy);assert not np.shares_memory(x,y)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
