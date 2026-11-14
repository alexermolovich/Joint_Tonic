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
 a,b=m.assign_weight_centroids(arr([-1,0,3]),np.array([True,True,False]),arr([-2,2]));equal(a,[0,0,-1],np.int64);equal(b,[-2,-2,0])
def example2(m):
 a,b=m.assign_weight_centroids(arr([1,4]),np.array([True,True]),arr([3,1,1]));equal(a,[1,0],np.int64);equal(b,[1,3])
def edges(m):
 a,b=m.assign_weight_centroids(arr([]),np.zeros(0,dtype=bool),arr([1]));equal(a,[],np.int64);equal(b,[])
 a,b=m.assign_weight_centroids(arr([1,2]),np.array([False,False]),arr([1]));equal(a,[-1,-1],np.int64);equal(b,[0,0])
def oracle(m):
 rng=np.random.default_rng(25);w=rng.normal(size=20000)[::2];active=np.arange(10000)%3!=0;c=np.linspace(2,-2,63);before=[w.copy(),active.copy(),c.copy()];a,b=m.assign_weight_centroids(w,active,c)
 indices=[min(range(63),key=lambda j:abs(float(v)-float(c[j]))) if active[i] else -1 for i,v in enumerate(w)];equal(a,indices,np.int64);equal(b,[float(c[j]) if j>=0 else 0 for j in indices]);preserve(before,[w,active,c]);assert not np.shares_memory(b,w)
def invalid(m):
 for w,a,c in [(arr([np.nan]),np.array([False]),arr([0])),(arr([1]),np.array([1]),arr([0])),(arr([1]),np.array([True]),arr([])),(arr([1]),np.array([True]),np.array([0])),(np.ones(100001),np.ones(100001,dtype=bool),arr([1])),(np.ones(100000),np.ones(100000,dtype=bool),np.ones(256))]:reject(lambda:m.assign_weight_centroids(w,a,c))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and numerical conventions','hidden',edges),('Independent oracle, realistic scale and preservation','hidden',oracle),('Invalid documented contract','hidden',invalid)]
