import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.action_value_gap([[1,3]],[[5]],[[True,True]],[[True]],2);assert_allclose(r['gap'],[3]);assert_array_equal(r['counts'],[[2,1]]);assert_array_equal(r['flagged'],[True])
def missing(m):
    assert not m.action_value_gap([[1,3]],[[5]],[[True,True]],[[True]],3)['flagged'][0]
    r=m.action_value_gap([[1]],[[5]],[[True]],[[False]],0);assert np.isnan(r['sample_mean'][0]) and np.isnan(r['gap'][0]);assert not r['flagged'][0]
def scale(m):
    l=np.ones((128,512))[:,::2];s=l*3;lm=np.ones_like(l,dtype=bool);sm=lm.copy();sm[:,::2]=False;r=m.action_value_gap(l,s,lm,sm,1);assert_allclose(r['gap'],2);assert_array_equal(r['counts'],np.tile([256,128],(128,1)));assert not np.shares_memory(r['logged_mean'],l)
def invalid(m):
    for args in [([[1]],[[2]],[[1]],[[True]],0),([[np.inf]],[[2]],[[False]],[[True]],0),([[1]],[[2]],[[True]],[[True]],-1)]:bad(lambda:m.action_value_gap(*args))
TESTS=[('Known action value gap','public',one),('Equality and unknown support','public',missing),('Scale independent reductions','hidden',scale),('Invalid inputs','hidden',invalid)]
