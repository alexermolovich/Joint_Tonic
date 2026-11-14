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

def example1(m):same(m.tolerance_reward(f([-1,0,1,2]),0,1,1,.5),[.5,1,1,.5])
def example2(m):same(m.tolerance_reward(f([-1,0,1]),0,0,0,.5),[0,1,0])
def edges(m):
 for dtype in [np.float32,np.float64]:
  x=np.array([-1,0,1],dtype=dtype);r=m.tolerance_reward(x,0,0,np.nextafter(0.,1.).item(),.5);same(r,[0,1,0]);assert r.dtype==np.float64 and np.isfinite(r).all()
 assert m.tolerance_reward(f([]),0,1,1,.5).shape==(0,)
 same(m.tolerance_reward(f([0,1,2]),0,0,1,.5),[1,.5,.0625])
 tiny=float(np.nextafter(0.,1.));same(m.tolerance_reward(f([0,tiny]),0,0,tiny,.5),[1,.5])
def oracle_scale(m):
 x=np.linspace(-3,4,400000)[::2];before=x.copy();r=m.tolerance_reward(x,0,1,2,.25)
 expected=[.25**(max(-float(v),float(v)-1,0)/2)**2 for v in x];same(r,expected);unchanged([before],[x]);assert not np.shares_memory(r,x)
def invalid(m):
 for values,lo,hi,margin,v in [(f([0]),1,0,1,.5),(f([0]),0,1,-1,.5),(f([0]),0,1,1,0),(f([0]),0,1,1,1),(f([np.nan]),0,1,1,.5),(f([0]),True,1,1,.5),(f([0]),0,1,np.float64(1),.5),(f([0]),0,1,10**1000,.5),(i([0]),0,1,1,.5)]:reject(lambda:m.tolerance_reward(values,lo,hi,margin,v))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
