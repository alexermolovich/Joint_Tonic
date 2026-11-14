import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.action_slice_metrics([True,False],[True,True],[0,0],2);assert_array_equal(r['count'],[2,0]);assert_allclose(r['invalid_rate'],[.5,np.nan],equal_nan=True);assert_allclose(r['success_rate'],[.5,np.nan],equal_nan=True)
def example2(m):
    r=m.action_slice_metrics([True,True],[False,True],[1,0],2);assert_array_equal(r['count'],[1,1]);assert_array_equal(r['invalid_rate'],[0,0]);assert_array_equal(r['success_rate'],[1,0])
def empty(m):
    r=m.action_slice_metrics(np.array([],dtype=bool),np.array([],dtype=bool),np.array([],dtype=int),3);assert_array_equal(r['count'],[0,0,0]);assert np.isnan(r['success_rate']).all()
def invalid(m):
    for a in [([1],[True],[0],1),([True],[True],[1],1),([True],[True],[-1],1),([True],[True],[0.],1),([True],[],[0],1),([True],[True],[0],False)]:bad(lambda:m.action_slice_metrics(*a))
TESTS=[('Invalid commands cannot succeed','public',example1),('Slice output order','public',example2),('Empty evidence','hidden',empty),('Invalid evaluation inputs','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    ids=np.arange(10000,dtype=np.int64)%10;v=ids%2==0;y=np.ones(10000,dtype=bool);r=m.action_slice_metrics(v,y,ids,12)
    assert_array_equal(r['count'][:10],np.full(10,1000));assert_array_equal(r['success_rate'][:10],np.arange(10)%2==0);assert np.isnan(r['invalid_rate'][10:]).all()

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
