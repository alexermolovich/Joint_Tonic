import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def example(m):
    z,s=m.feature_drift(np.array([[0.],[2.]]),np.array([[1.],[3.]]));assert_allclose(z,[1/1.000001**.5]);assert_allclose(s,1/1.000001**.5)
def constant(m):
    z,s=m.feature_drift(np.array([[4.,4.]]),np.array([[4.001,4.]]));assert_allclose(z,[1,0],atol=1e-9);assert_allclose(s,2**-.5,atol=1e-9)
def oracle(m):
    r=np.random.default_rng(71);a=r.normal(size=(37,11));b=r.normal(1,2,(61,11));copy=a.copy();z,s=m.feature_drift(a,b)
    expected=[]
    for j in range(11):
        mean=sum(float(x) for x in a[:,j])/37;var=sum((float(x)-mean)**2 for x in a[:,j])/37;expected.append((sum(float(x) for x in b[:,j])/61-mean)/(var+1e-6)**.5)
    assert_allclose(z,expected);assert_allclose(s,(sum(x*x for x in expected)/11)**.5);assert_array_equal(a,copy);assert type(s) is float
def invariants(m):
    a=np.array([[0.,2.],[2,0]]);b=np.array([[2.,0.],[4,-2.]])
    z,s=m.feature_drift(a,b);z2,s2=m.feature_drift(a[::-1]+4,b[::-1]+4);assert_allclose(z,z2);assert_allclose(s,s2);assert s>0
def invalid(m):
    for a,b in [(np.empty((0,2)),np.ones((1,2))),(np.ones((1,2)),np.ones((1,3))),(np.ones((1,2),dtype=np.float32),np.ones((1,2))),(np.array([[np.nan]]),np.ones((1,1)))]:
        with np.testing.assert_raises(ValueError):m.feature_drift(a,b)
TESTS=[('Reference population scale','public',example),('Variance floor','public',constant),('Scalar moment oracle','hidden',oracle),('Permutation translation and opposing channels','hidden',invariants),('Validation','hidden',invalid)]
