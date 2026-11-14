import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    a,p=m.route_action_heads([[2],[2]],[0,1],[[[1,2]],[[3,4]]],[[1,1],[1,1]],[1,2]);assert_array_equal(a,[[3,0],[7,9]]);assert_array_equal(p,[[1,0],[1,1]])
def zero(m):
    a,p=m.route_action_heads([[0]],[0],[[[5]]],[[0]],[1]);assert_array_equal(a,[[0]]);assert p.all()
def scale(m):
    x=np.arange(128*64.).reshape(128,64)[:,::2];w=np.ones((3,32,8));ids=np.arange(128)%3;n=np.array([1,4,8]);a,p=m.route_action_heads(x,ids,w,np.zeros((3,8)),n);assert_allclose(a,np.where(np.arange(8)<n[ids,None],x.sum(1)[:,None],0));assert not np.shares_memory(a,x)
def invalid(m):
    for a in [([[1]],[1],[[[1]]],[[0]],[1]),([[1]],[0],[[[1]]],[[0]],[0]),([[1]],[0],[[[1]]],[[0]],[2]),([[1]],[0.],[[[1]]],[[0]],[1])]:bad(lambda:m.route_action_heads(*a))
TESTS=[('Dataset routing','public',one),('Valid zero action','public',zero),('Scale and padded widths','hidden',scale),('Invalid heads','hidden',invalid)]
