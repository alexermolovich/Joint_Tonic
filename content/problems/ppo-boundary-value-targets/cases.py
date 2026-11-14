import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def continuation(m):assert_array_equal(m.boundary_value_targets([[1,2]],[[10,20]],[[False,False]],[[False,False]],[[True,True]],.5,1),[[7,12]])
def boundaries(m):
    assert_array_equal(m.boundary_value_targets([[1,2]],[[10,20]],[[False,False]],[[True,False]],[[True,True]],.5,1),[[6,12]])
    assert_array_equal(m.boundary_value_targets([[1,2]],[[10,20]],[[True,False]],[[False,False]],[[True,True]],.5,1),[[1,12]])
def scale(m):
    r=np.ones((32,2048))[:,::2];v=np.zeros_like(r);no=np.zeros_like(r,dtype=bool);valid=np.ones_like(no);out=m.boundary_value_targets(r,v,no,no,valid,1,1);assert_array_equal(out,np.tile(np.arange(1024,0,-1),(32,1)));assert not np.shares_memory(out,r)
    assert_array_equal(m.boundary_value_targets([[5,9]],[[2,4]],[[False,False]],[[False,False]],[[True,False]],.5,.5),[[6,0]])
    assert not m.boundary_value_targets([[1]],[[1]],[[False]],[[False]],[[False]],1,1).any()
def invalid(m):
    for d,c,v in [([[True]],[[True]],[[True]]),([[True]],[[False]],[[False]]),([[False,False]],[[False,False]],[[False,True]])]:
        shape=np.asarray(v).shape;bad(lambda:m.boundary_value_targets(np.ones(shape),np.ones(shape),d,c,v,.9,1))
TESTS=[('Within-rollout continuation','public',continuation),('Terminal versus time limit','public',boundaries),('Scale partial prefixes and empty support','hidden',scale),('Invalid boundary flags','hidden',invalid)]

def lambda_mix(m):
    args=[[[1,2]],[[10,20]],[[False,False]],[[False,False]],[[True,True]],.5]
    assert_array_equal(m.boundary_value_targets(*args,.5),[[6.5,12]])
    assert_array_equal(m.boundary_value_targets(*args,0),[[6,12]])
TESTS.append(("Fractional lambda and one-step endpoint", "hidden", lambda_mix))
