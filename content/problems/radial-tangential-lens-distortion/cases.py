import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def radial(m):
    assert_allclose(m.distort_normalized_points([[1,0],[0,1]],[.1,0,0,0,0]),[[1.1,0],[0,1.1]])
def tangential(m):
    assert_allclose(m.distort_normalized_points([[1,0]],[0,0,.1,.2,0]),[[1.6,.1]])
def terms(m):
    assert_allclose(m.distort_normalized_points([[1,1]],[.1,.2,.3,.4,.5]),[[8.2,8.0]])
def identity_and_symmetry(m):
    p=np.random.default_rng(13).uniform(-2,2,(100,2)); old=p.copy(); out=m.distort_normalized_points(p,np.zeros(5)); assert_array_equal(out,p); assert not np.shares_memory(out,p)
    c=[.1,.01,0,0,.001]; assert_allclose(m.distort_normalized_points(-p,c),-m.distort_normalized_points(p,c)); assert_array_equal(p,old)
    assert m.distort_normalized_points(np.empty((0,2)),c).shape==(0,2)
def invalid(m):
    for p,c in [([1,2],[0]*5),([[11,0]],[0]*5),([[0,0]],[2,0,0,0,0]),([[0,0]],[0]*4),([[np.nan,0]],[0]*5),([[True,False]],[0]*5)]:
        with np.testing.assert_raises(ValueError): m.distort_normalized_points(p,c)
TESTS=[('Radial displacement','public',radial),('Tangential displacement','public',tangential),('All five coefficients','hidden',terms),('Identity symmetry and empty batch','hidden',identity_and_symmetry),('Invalid calibration input','hidden',invalid)]
