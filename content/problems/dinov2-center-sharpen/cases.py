import numpy as np
from numpy.testing import assert_allclose,assert_array_equal


def centering(m):
    assert_allclose(m.center_sharpen(np.array([[2.,0.],[0.,2.]]),np.array([1.,0.]),1.),[[.7310585786,.2689414214],[.0474258732,.9525741268]],atol=1e-9)


def sharpening(m):
    assert_allclose(m.center_sharpen(np.array([[1.,0.]]),np.zeros(2),.5),[[.880797078,.119202922]],atol=1e-9)


def single_class(m):assert_array_equal(m.center_sharpen(np.array([[99.],[-10.]]),np.array([10.]),1e-4),[[1.],[1.]])


def stable(m):
    x=np.array([[1e6,-1e6],[-1e6,1e6],[1e6,1e6]])
    y=m.center_sharpen(x,np.zeros(2),1e-4)
    assert_allclose(y,[[1,0],[0,1],[.5,.5]],atol=1e-9)


def invariance(m):
    rng=np.random.default_rng(20261113);x=rng.normal(size=(11,7));c=rng.normal(size=7);old=x.copy();oldc=c.copy()
    y=m.center_sharpen(x,c,.7)
    assert_allclose(y,m.center_sharpen(x+40,c,.7),rtol=1e-7,atol=1e-9)
    assert_allclose(y.sum(1),1,atol=1e-9)
    assert_allclose(m.center_sharpen(x[:,::-1],c[::-1],.7),y[:,::-1],atol=1e-9)
    assert_array_equal(x,old);assert_array_equal(c,oldc)
    assert not np.shares_memory(y,x) and not np.shares_memory(y,c)


def invalid(m):
    with np.testing.assert_raises(TypeError):m.center_sharpen([[1.]],np.ones(1),1.)
    for x,c,t in [(np.zeros((0,2)),np.zeros(2),1),(np.zeros((1,2),dtype=np.float32),np.zeros(2),1),(np.zeros((1,2)),np.zeros(3),1),(np.full((1,2),np.nan),np.zeros(2),1),(np.zeros((1,2)),np.zeros(2),0),(np.zeros((1,2)),np.zeros(2),True),(np.zeros((1,2)),np.zeros(2),10**1000)]:
        with np.testing.assert_raises(ValueError):m.center_sharpen(x,c,t)


TESTS=[("Centered teacher rows","public",centering),("Sharper temperature","public",sharpening),("One prototype","public",single_class),
       ("Large stable logits","hidden",stable),("Shift and layout invariants","hidden",invariance),("Validation","hidden",invalid)]
