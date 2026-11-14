import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def examples(m):
    assert_array_equal(m.sample_task_balanced([2,2,5],[[.2,.8],[.8,.2]]),[1,2])
def second(m):
    assert_array_equal(m.sample_task_balanced([7,7],[[0,0],[.99,.99]]),[0,1])
def groups(m):
    ids=np.array([9,1,9,4]);u=np.array([[0,0],[1/3,0],[2/3,0],[.99,.99]])
    a=ids.copy();b=u.copy();out=m.sample_task_balanced(ids,u)
    assert_array_equal(out,[1,3,0,2]);assert out.dtype==np.int64;assert_array_equal(ids,a);assert_array_equal(u,b)
    assert m.sample_task_balanced([1],np.empty((0,2))).shape==(0,)
def invalid(m):
    for ids,u in [([],[[0,0]]),([1.],[[0,0]]),([-1],[[0,0]]),([1],[[1,0]]),([1],[[-.1,0]]),([1],[[0]]),([True],[[0,0]]),([1],[[np.nan,0]])]:bad(lambda:m.sample_task_balanced(ids,u))
TESTS=[('Two task draws','public',examples),('Single task','public',second),('Sorted groups and empty draws','hidden',groups),('Invalid sampling inputs','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    ids=np.arange(10000,dtype=np.int64)[::2]%5;u=np.tile([[.41,.9]],(5000,1));a=ids.copy();b=u.copy();r=m.sample_task_balanced(ids,u)
    assert r.shape==(5000,) and np.all(ids[r]==2);assert_array_equal(ids,a);assert_array_equal(u,b);assert not np.shares_memory(r,ids)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
