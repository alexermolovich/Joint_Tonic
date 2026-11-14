import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.soft_state_value([[2,4]],[[-1,-2]],[[True,True]],.5);assert_allclose(r['values'],[3.75]);assert_array_equal(r['counts'],[2]);assert r['counts'].dtype==np.int64

def empty(m):assert_array_equal(m.soft_state_value([[2,4]],[[-1,-2]],[[False,False]],.5)['values'],[0])
def scale(m):
    q=np.ones((128,512))[:,::2]*3;p=np.ones_like(q)*2;valid=np.ones_like(q,dtype=bool);valid[:,::2]=False;r=m.soft_state_value(q,p,valid,1);assert_array_equal(r['values'],np.ones(128));assert_array_equal(r['counts'],np.full(128,128));assert not np.shares_memory(r['values'],q)
def invalid(m):
    for a in [([[1]],[[101]],[[True]],1),([[1]],[[0]],[[1]],1),([[1]],[[0]],[[True]],True)]:bad(lambda:m.soft_state_value(*a))
TESTS=[('Soft sample expectation','public',one),('No action samples','public',empty),('Scale positive density and masks','hidden',scale),('Invalid value contract','hidden',invalid)]
