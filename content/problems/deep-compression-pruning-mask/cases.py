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
 a,b=m.prune_weights(arr([[-.5,.2],[0,1]]),.5);equal(a,[[True,False],[False,True]],bool);equal(b,[[-.5,0],[0,1]])
def example2(m):
 a,b=m.prune_weights(arr([[0,-1]]),0);equal(a,[[True,True]],bool);equal(b,[[0,-1]])
def edges(m):
 a,b=m.prune_weights(np.array([[1e-38,-1e-38]],dtype=np.float32),1e-39);equal(a,[[True,True]],bool);assert b.dtype==np.float64
 a,b=m.prune_weights(arr([[-1e6,1e6,0]]),1e6);equal(a,[[True,True,False]],bool)
def oracle(m):
 x=np.arange(-262144,262144,dtype=float).reshape(512,1024)[:,::2];before=x.copy();a,b=m.prune_weights(x,8192);wanted=np.array([[abs(float(v))>=8192 for v in row] for row in x]);equal(a,wanted,bool);equal(b,np.where(wanted,x,0));np.testing.assert_array_equal(x,before);assert not np.shares_memory(b,x)
def invalid(m):
 for w,t in [(arr([[1]]),True),(arr([[1]]),-1),(arr([[1]]),float('inf')),(np.empty((0,1)),0),(np.array([[1]]),0),(arr([[np.nan]]),0)]:reject(lambda:m.prune_weights(w,t))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
