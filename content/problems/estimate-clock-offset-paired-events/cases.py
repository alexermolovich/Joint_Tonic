import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    o,r=m.estimate_clock_offset([0,1,2],[2,3,11]); assert o==2.; assert_allclose(r,[0,0,7])
def even(m):
    o,r=m.estimate_clock_offset([1,2],[0,3]); assert o==0.; assert_allclose(r,[-1,1])
def invariants(m):
    a=np.arange(101,dtype=np.float64); b=a-3; b[-1]+=50; ac=a.copy(); bc=b.copy()
    o,r=m.estimate_clock_offset(a,b); assert o==-3.; assert r.dtype==np.float64; assert r[-1]==50
    assert_array_equal(a,ac); assert_array_equal(b,bc)
    p=np.arange(101)[::-1]; o2,r2=m.estimate_clock_offset(a[p]+10,b[p]+10); assert o2==o; assert_array_equal(r2,r[p])
def single(m):
    o,r=m.estimate_clock_offset([9],[1]); assert isinstance(o,float) and o==-8; assert_allclose(r,[0])
def invalid(m):
    for a,b in [([],[]),([0],[1,2]),([[0]],[[1]]),([np.inf],[1]),([True],[1]),(['1'],[1]),([0],[1j])]:
        with np.testing.assert_raises(ValueError): m.estimate_clock_offset(a,b)
TESTS=[('Outlier robust estimate','public',example),('Even sample median','public',even),('Translation and permutation invariance','hidden',invariants),('Single event','hidden',single),('Invalid pairs','hidden',invalid)]
