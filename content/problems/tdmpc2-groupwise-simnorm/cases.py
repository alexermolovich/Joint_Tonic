import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def equal(m):assert_array_equal(m.simnorm([[0,0,1,1]],2),[[.5,.5,.5,.5]])
def ratios(m):assert_allclose(m.simnorm([[0,np.log(3),1000,1000]],2),[[.25,.75,.5,.5]])
def scale(m):
    rng=np.random.default_rng(543);x=rng.uniform(-1e6,1e6,(2048,512))[:,::2];before=x.copy();r=m.simnorm(x,8);assert_allclose(r.reshape(2048,32,8).sum(axis=-1),1);assert np.isfinite(r).all();assert_array_equal(x,before);assert not np.shares_memory(r,x)
    x=np.array([[1,2,3,4.]]);assert_allclose(m.simnorm(x,2),m.simnorm(x+np.array([[100,100,-100,-100]]),2));assert_array_equal(m.simnorm(x,1),np.ones_like(x));assert m.simnorm(np.empty((0,4)),2).shape==(0,4)
def invalid(m):
    for x,g in [([[1,2,3]],2),([[0]],True),([[np.nan]],1),([[0]],0)]:bad(lambda:m.simnorm(x,g))
TESTS=[('Independent group normalization','public',equal),('Group ratio and stable shift','public',ratios),('Large logits noncontiguous scale and invariance','hidden',scale),('Invalid simplex layout','hidden',invalid)]
