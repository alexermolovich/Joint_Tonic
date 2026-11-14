import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def wrap(m):
    r=m.phase_alignment([[.99]],[[.01]],[[True]],.03);assert_allclose(r['error'],[[-.02]]);assert not r['misaligned'][0,0];assert_allclose(r['mean_absolute'],[.02])
def tie(m):
    r=m.phase_alignment([[.5,0]],[[0,0]],[[True,False]],.5);assert_allclose(r['error'],[[-.5,np.nan]]);assert not r['misaligned'].any();assert_array_equal(r['counts'],[1])
def scale(m):
    o=np.full((128,512),.125)[:,::2];r=m.phase_alignment(o,np.full_like(o,.875),np.ones_like(o,bool),.25);assert_allclose(r['error'],.25);assert not r['misaligned'].any();assert not np.shares_memory(r['error'],o)
    r=m.phase_alignment([[0]],[[0]],[[False]],0);assert np.isnan(r['mean_absolute'][0]) and r['counts'][0]==0
def invalid(m):
    for args in [([[1]],[[0]],[[True]],0),([[0]],[[0]],[[1]],0),([[0]],[[0]],[[True]],.6)]:bad(lambda:m.phase_alignment(*args))
TESTS=[('Cyclic wrap','public',wrap),('Half-cycle and missing observation','public',tie),('Scale equality and empty row','hidden',scale),('Invalid phases','hidden',invalid)]
