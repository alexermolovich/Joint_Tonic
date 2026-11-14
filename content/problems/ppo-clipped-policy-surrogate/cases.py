import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def signed(m):
    r=m.clipped_surrogate([[np.log(1.5),np.log(1.5)]],[[0,0]],[[1,-1]],[[True,True]],.2);assert_allclose(r['terms'],[[1.2,-1.5]]);assert_allclose(r['objective'],-.15);assert_allclose(r['loss'],.15)
def empty(m):
    r=m.clipped_surrogate([[1]],[[0]],[[8]],[[False]],.2);assert r['objective']==r['loss']==0;assert_array_equal(r['terms'],[[0]])
def scale(m):
    x=np.zeros((64,2048))[:,::2];a=np.tile([1.,-1.],(64,512));mask=np.ones_like(x,dtype=bool);r=m.clipped_surrogate(x,x,a,mask,.2);assert_array_equal(r['terms'],a);assert r['loss']==0;assert not np.shares_memory(r['terms'],a)
def invalid(m):
    for args in [([[101]],[[0]],[[1]],[[True]],.2),([[40.1]],[[0]],[[1]],[[True]],.2),([[0]],[[0]],[[1]],[[1]],.2),([[0]],[[0]],[[1]],[[True]],True),([[0]],[[0]],[[np.nan]],[[False]],.2)]:bad(lambda:m.clipped_surrogate(*args))
TESTS=[('Signed clipping branches','public',signed),('No valid support','public',empty),('Scale and independent storage','hidden',scale),('Invalid policy batch','hidden',invalid)]
