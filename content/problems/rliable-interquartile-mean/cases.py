"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import math
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')

def same(a,b):np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)
def f(x):return np.array(x,dtype=np.float64)
def i(x):return np.array(x,dtype=np.int64)
def b(x):return np.array(x,dtype=bool)

def unchanged(before,after):
    for x,y in zip(before,after):np.testing.assert_array_equal(x,y)

def example1(m):assert m.interquartile_score(f([[0,1,2,3],[4,5,6,100]]))==3.5
def example2(m):same(m.interquartile_score(f([[1,2,100]])),103/3)
def edges(m):
 for values in [[[5]],[[4,2]],[[0,0,0,100]],[[3,3,3,3,3]],[[1,2,3,100,200]]]:
  x=np.array(values,dtype=np.float32);z=sorted(map(float,x.ravel()));k=len(z)//4
  y=m.interquartile_score(x);assert type(y) is float;same(y,sum(z[k:len(z)-k])/(len(z)-2*k))
def oracle_scale(m):
 rng=np.random.default_rng(920);x=rng.integers(-10000,10000,size=(400,1000)).astype(np.float64)[:,::2];before=x.copy()
 z=sorted(x.ravel().tolist());k=len(z)//4;same(m.interquartile_score(x),math.fsum(z[k:len(z)-k])/(len(z)-2*k));unchanged([before],[x])
def invalid(m):
 for x in [[],f([]),np.ones((1,1),dtype=np.int64),f([[np.nan]]),f([[np.inf]]),f([[1e6+1]]),np.zeros((0,1)),np.zeros((1,2049)),np.zeros((1001,1000))]:reject(lambda:m.interquartile_score(x))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
