import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def examples(m):
    assert_array_equal(m.match_timestamps([0,1,2],[.1,.5,1.9],.2),[0,-1,2])
def ties(m):
    assert_array_equal(m.match_timestamps([0,2],[1,0,2],1),[0,0,1])
def empty(m):
    assert_array_equal(m.match_timestamps([],[-2,3],0),[-1,-1])
    out=m.match_timestamps([1],[],1); assert out.shape==(0,) and out.dtype==np.int64
def oracle(m):
    rng=np.random.default_rng(20261113); r=np.sort(rng.uniform(-10,10,99)); q=rng.uniform(-12,12,500)
    before=r.copy(); expected=[]
    for x in q:
        j=min(range(len(r)),key=lambda i:(abs(r[i]-x),i)); expected.append(j if abs(r[j]-x)<=.3 else -1)
    assert_array_equal(m.match_timestamps(r,q,.3),expected); assert_array_equal(r,before)
def invalid(m):
    for args in [([1,1],[0],1),([1,0],[0],1),([[1]],[0],1),([0],[[0]],1),([0],[0],-1),([0],[0],[1]),([np.nan],[0],1),([True],[0],1),([0],[1j],1),([0],[0],np.inf)]:
        with np.testing.assert_raises(ValueError): m.match_timestamps(*args)
TESTS=[('Nearest within tolerance','public',examples),('Tie and exact matches','public',ties),('Empty sequences','hidden',empty),('Independent exhaustive oracle','hidden',oracle),('Invalid times','hidden',invalid)]
