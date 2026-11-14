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
 x,w=m.rescale_linear_channels(arr([[2,8]]),arr([[3],[4]]),arr([2,4]));equal(x,[[1,2]]);equal(w,[[6],[16]]);equal(x@w,[[38]])
def example2(m):
 x,w=m.rescale_linear_channels(arr([[0,-3]]),arr([[5,1],[2,-1]]),arr([1,.5]));equal(x,[[0,-6]]);equal(w,[[5,1],[1,-.5]])
def edges(m):
 x=np.array([[1e-38]],dtype=np.float32);w=np.array([[2e-38]],dtype=np.float32);s=arr([1e6]);a,b=m.rescale_linear_channels(x,w,s)
 assert a.dtype==b.dtype==np.float64;assert a[0,0]==float(x[0,0])/1e6;assert b[0,0]==float(w[0,0])*1e6
 a,b=m.rescale_linear_channels(arr([[1e6]]),arr([[1e6]]),arr([1e-6]));equal(a,[[1e12]]);equal(b,[[1]])
def oracle(m):
 rng=np.random.default_rng(21);x=rng.normal(size=(256,128))[:,::2];w=rng.normal(size=(128,32))[::2];s=np.linspace(.01,10,64);before=[x.copy(),w.copy(),s.copy()]
 a,b=m.rescale_linear_channels(x,w,s);equal(a,[[float(x[i,j])/float(s[j]) for j in range(64)] for i in range(256)]);equal(b,[[float(w[j,k])*float(s[j]) for k in range(32)] for j in range(64)]);equal(a@b,x@w);preserve(before,[x,w,s]);assert not np.shares_memory(a,x)
def invalid(m):
 for s in [arr([0]),arr([-1]),arr([1e-7]),arr([np.nan]),arr([1,2]),np.array([1])]:reject(lambda:m.rescale_linear_channels(arr([[1]]),arr([[1]]),s))
 reject(lambda:m.rescale_linear_channels(arr([[1,2]]),arr([[1]]),arr([1,1])))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
