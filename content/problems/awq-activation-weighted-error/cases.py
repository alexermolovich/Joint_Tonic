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
 a,b,k=m.compare_quantized_candidates(arr([[10,1]]),arr([[0],[0]]),arr([[[1],[0]],[[0],[2]]]));equal(a,[.5,2]);equal(b,[100,4]);assert k==1 and type(k) is int
def example2(m):
 a,b,k=m.compare_quantized_candidates(arr([[1,1]]),arr([[0],[0]]),arr([[[1],[-1]],[[0],[0]]]));equal(a,[1,0]);equal(b,[0,0]);assert k==0
def edges(m):
 a,b,k=m.compare_quantized_candidates(np.zeros((1,1),dtype=np.float32),arr([[1]]),arr([[[8]],[[1]]]));equal(a,[49,0]);equal(b,[0,0]);assert k==0

def oracle(m):
 rng=np.random.default_rng(28);x=rng.normal(size=(32,128))[:,::2];w=rng.normal(size=(64,16));c=rng.normal(size=(8,64,32))[:,:,::2];before=[x.copy(),w.copy(),c.copy()];a,b,k=m.compare_quantized_candidates(x,w,c)
 ew=[];ey=[]
 for z in c:
  delta=[[float(z[j,t])-float(w[j,t]) for t in range(16)] for j in range(64)]
  ew.append(sum(v*v for row in delta for v in row)/(64*16))
  out=[sum(float(x[i,j])*delta[j][t] for j in range(64)) for i in range(32) for t in range(16)];ey.append(sum(v*v for v in out)/(32*16))
 equal(a,ew);equal(b,ey);assert k==min(range(8),key=lambda i:ey[i]);preserve(before,[x,w,c])
def invalid(m):
 reject(lambda:m.compare_quantized_candidates(arr([[1]]),arr([[1]]),np.empty((0,1,1))))
 reject(lambda:m.compare_quantized_candidates(arr([[1]]),arr([[1]]),arr([[[np.nan]]])))
 reject(lambda:m.compare_quantized_candidates(np.ones((256,256)),np.ones((256,64)),np.ones((16,256,64))))
 reject(lambda:m.compare_quantized_candidates(arr([[1]]),arr([[1]]),np.ones((1,1,2))))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
