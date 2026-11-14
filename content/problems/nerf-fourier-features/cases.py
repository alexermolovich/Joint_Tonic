import numpy as np
from numpy.testing import assert_allclose,assert_array_equal


def one_level(m):assert_allclose(m.fourier_encode(np.array([[0.,.5,1.]]),1),[[0,1,0,1,0,-1]],atol=1e-9)


def two_levels(m):
    r=np.sqrt(.5)
    assert_allclose(m.fourier_encode(np.array([[.25,0.,0.]]),2),[[r,0,0,r,1,1,1,0,0,0,1,1]],atol=1e-9)


def empty(m):
    assert m.fourier_encode(np.empty((0,3)),4).shape==(0,24)
    assert m.fourier_encode(np.ones((5,3)),0).shape==(5,0)


def oracle(m):
    rng=np.random.default_rng(20261113);x=rng.normal(size=(29,3));old=x.copy()
    expected=np.array([[f((2**ell)*np.pi*c) for ell in range(5) for f in (np.sin,np.cos) for c in p] for p in x])
    y=m.fourier_encode(x,5)
    assert_allclose(y,expected,atol=1e-9,rtol=1e-7);assert_array_equal(x,old)
    assert not np.shares_memory(x,y)


def layout_bounds(m):
    x=np.array([[1e4,-1e4,0.],[.1,-.2,.3]])[:,::-1]
    y=m.fourier_encode(x,10)
    assert y.shape==(2,60) and y.dtype==np.float64
    assert np.isfinite(y).all() and np.max(np.abs(y))<=1
    for ell in range(10):assert_allclose(y[:,ell*6:ell*6+3]**2+y[:,ell*6+3:ell*6+6]**2,1,atol=1e-9)


def invalid(m):
    with np.testing.assert_raises(TypeError):m.fourier_encode([[0,0,0]],1)
    for x,l in [(np.zeros((1,3),dtype=np.float32),1),(np.zeros((1,2)),1),(np.full((1,3),np.inf),1),(np.full((1,3),1e5),1),(np.zeros((1,3)),True),(np.zeros((1,3)),-1),(np.zeros((1,3)),11)]:
        with np.testing.assert_raises(ValueError):m.fourier_encode(x,l)


TESTS=[("One frequency","public",one_level),("Two frequencies","public",two_levels),("Empty encodings","public",empty),
       ("Independent channel oracle","hidden",oracle),("Noncontiguous bounded phase","hidden",layout_bounds),("Validation","hidden",invalid)]
