"""Original deterministic synthetic fixtures; CC0-1.0."""
import numpy as np
import math

def arr(x):return np.array(x,dtype=np.float64)
def equal(actual,expected,dtype=np.float64):
    assert isinstance(actual,np.ndarray) and actual.dtype==np.dtype(dtype)
    assert actual.shape==np.asarray(expected).shape
    np.testing.assert_allclose(actual,expected,rtol=1e-9,atol=1e-10)
def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def preserve(before,after):
    for a,b in zip(before,after):np.testing.assert_array_equal(a,b)

def example1(m):
 a,w=m.calibration_channel_ranges(arr([[1,-4],[3,2]]),arr([[2,-1],[0,-5]]));equal(a,[3,4]);equal(w,[2,5])
def example2(m):
 a,w=m.calibration_channel_ranges(arr([[0,2]]),arr([[0],[3]]));equal(a,[0,2]);equal(w,[0,3])
def edges(m):
 x=np.array([[1e-38,-2e-38]],dtype=np.float32);w=arr([[0],[-1e-250]]);a,b=m.calibration_channel_ranges(x,w)
 np.testing.assert_array_equal(a,np.abs(x.astype(float))[0]);np.testing.assert_array_equal(b,[0,1e-250])
def oracle(m):
 rng=np.random.default_rng(19);x=rng.normal(size=(512,128))[::2,::2];w=rng.normal(size=(64,64))[:,::2];before=[x.copy(),w.copy()]
 a,b=m.calibration_channel_ranges(x,w);equal(a,[max(abs(float(x[i,j])) for i in range(256)) for j in range(64)]);equal(b,[max(abs(float(w[j,k])) for k in range(32)) for j in range(64)]);preserve(before,[x,w]);assert not np.shares_memory(a,x)
def invalid(m):
 for x,w in [(arr([]).reshape(0,1),arr([[1]])),(arr([[1,2]]),arr([[1]])),(np.array([[1]]),arr([[1]])),(arr([[np.nan]]),arr([[1]])),(arr([[1]]),arr([[np.inf]])),(arr([[1e7]]),arr([[1]])),(np.ones((1001,1000)),np.ones((1000,1)))]:reject(lambda:m.calibration_channel_ranges(x,w))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
