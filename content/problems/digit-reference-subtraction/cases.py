import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def image(m):
    x=np.array([[0,.2],[.1,.4]])[None,:,:,None];r=m.tactile_difference(x,np.zeros((2,2,1)),np.ones((2,2),bool),.15);assert_array_equal(r['mask'],[[[False,True],[False,True]]]);assert_array_equal(r['change'],x[...,0])
def sign(m):
    r=m.tactile_difference([[[[.2]]]],[[[.8]]],[[True]],.5);assert_allclose(r['difference'],[[[[-.6]]]]);assert_allclose(r['change'],[[[.6]]])
def scale(m):
    x=np.zeros((32,64,128,3))[:,:,::2,:];x[...,0]=1;ref=np.zeros((64,64,3));ref[...,1]=1;roi=np.ones((64,64),bool);roi[:,::2]=False;r=m.tactile_difference(x,ref,roi,2/3);assert_allclose(r['change'][:,:,1::2],2/3);assert not r['mask'].any();assert not np.shares_memory(r['difference'],x);assert_array_equal(x[...,0],np.ones((32,64,64)))
    assert not m.tactile_difference(x,ref,np.zeros_like(roi),0)['change'].any()
def invalid(m):
    for a in [([[[[2]]]],[[[0]]],[[False]],0),([[[[0]]]],[[[np.nan]]],[[False]],0),([[[[0]]]],[[[0]]],[[1]],0)]:bad(lambda:m.tactile_difference(*a))
TESTS=[('Optical change mask','public',image),('Signed subtraction','public',sign),('Scale ROI channel reduction and strict threshold','hidden',scale),('Invalid masked image data','hidden',invalid)]
