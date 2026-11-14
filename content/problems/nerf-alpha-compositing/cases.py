import numpy as np
from numpy.testing import assert_allclose,assert_array_equal


def halves(m):
    w,b=m.alpha_compositing_weights(np.array([[np.log(2),np.log(2),0.]]),np.array([[1.,1.,2.]]))
    assert_allclose(w,[[.5,.25,0]],atol=1e-9);assert_allclose(b,[.25])


def metric_lengths(m):
    w,b=m.alpha_compositing_weights(np.array([[0.,np.log(4),np.log(2)]]),np.array([[3.,.5,1.]]))
    assert_allclose(w,[[0,.5,.25]],atol=1e-9);assert_allclose(b,[.25])


def transparent(m):
    w,b=m.alpha_compositing_weights(np.ones((2,3)),np.zeros((2,3)))
    assert_array_equal(w,np.zeros((2,3)));assert_array_equal(b,[1,1])


def tiny(m):
    q=np.array([[1e-18,1e-20]])
    w,b=m.alpha_compositing_weights(q,np.ones_like(q))
    assert_allclose(w,q,rtol=1e-10,atol=0)
    assert_allclose(b,[1],atol=1e-15)


def opaque(m):
    w,b=m.alpha_compositing_weights(np.array([[1e6,2.,3.]]),np.array([[1e6,1.,1.]]))
    assert_array_equal(w,[[1,0,0]]);assert_array_equal(b,[0])


def sequential_oracle(m):
    rng=np.random.default_rng(20261113)
    d=rng.uniform(0,2,(12,37));step=rng.uniform(0,.2,(12,37))
    expected=np.empty_like(d);background=[]
    for r in range(12):
        mass=1.
        for i in range(37):
            opacity=-np.expm1(-d[r,i]*step[r,i])
            expected[r,i]=mass*opacity
            mass*=np.exp(-d[r,i]*step[r,i])
        background.append(mass)
    w,b=m.alpha_compositing_weights(d[:,::-1][:,::-1],step)
    assert_allclose(w,expected,rtol=1e-6,atol=1e-9)
    assert_allclose(b,background,rtol=1e-6,atol=1e-9)
    assert_allclose(w.sum(1)+b,np.ones(12),atol=1e-9)


def storage_and_single(m):
    d=np.array([[np.log(3)]]);step=np.ones((1,1));old=d.copy()
    w,b=m.alpha_compositing_weights(d,step)
    assert w.shape==(1,1) and b.shape==(1,) and w.dtype==b.dtype==np.float64
    assert_allclose(w,[[2/3]]);assert_allclose(b,[1/3])
    assert not np.shares_memory(w,d) and not np.shares_memory(b,d)
    assert_array_equal(d,old)


def invalid(m):
    with np.testing.assert_raises(TypeError):m.alpha_compositing_weights([[1.]],np.ones((1,1)))
    for d,s in [(np.ones((1,1),dtype=np.float32),np.ones((1,1))), (np.empty((0,1)),np.empty((0,1))), (np.ones((1,2)),np.ones((1,1))), (np.array([[-1.]]),np.ones((1,1))), (np.array([[np.inf]]),np.ones((1,1))), (np.ones((1,1)),np.array([[1e6+1]]))]:
        with np.testing.assert_raises(ValueError):m.alpha_compositing_weights(d,s)


TESTS=[("Two half-opaque intervals","public",halves),("Metric interval lengths","public",metric_lengths),("Transparent ray","public",transparent),
       ("Tiny positive opacity","hidden",tiny),("Opaque prefix","hidden",opaque),("Sequential mass oracle","hidden",sequential_oracle),
       ("Single interval and storage","hidden",storage_and_single),("Validation","hidden",invalid)]
