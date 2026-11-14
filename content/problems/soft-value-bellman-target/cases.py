import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):assert_array_equal(m.soft_bellman_target([[1,1]],[[4,4]],[[False,True]],[[True,True]],.5),[[3,1]])
def masked(m):assert_array_equal(m.soft_bellman_target([[1,1]],[[4,4]],[[False,False]],[[True,False]],.5),[[3,0]])
def scale(m):
    r=np.ones((64,2048))[:,::2];v=r*8;d=np.zeros_like(r,dtype=bool);d[:,::2]=True;out=m.soft_bellman_target(r,v,d,np.ones_like(d),.5);assert_array_equal(out[:,::2],np.ones((64,512)));assert_array_equal(out[:,1::2],np.full((64,512),5));assert not np.shares_memory(out,r)
def invalid(m):
    for a in [([[1]],[[1]],[[1]],[[True]],.5),([[1]],[[1,2]],[[False]],[[True]],.5),([[np.nan]],[[1]],[[False]],[[False]],.5),([[1]],[[1]],[[False]],[[True]],2)]:bad(lambda:m.soft_bellman_target(*a))
TESTS=[('Terminal bootstrap mask','public',one),('Time limit and padding','public',masked),('Scale and independent target','hidden',scale),('Invalid transitions','hidden',invalid)]
