import numpy as np
from numpy.testing import assert_array_equal


def one_cloud(m):
    y=m.concat_local_global(np.array([[[1.,2.],[3.,4.]]]),np.array([[10.,20.,30.]]))
    assert_array_equal(y,[[[1,2,10,20,30],[3,4,10,20,30]]])


def two_clouds(m):
    y=m.concat_local_global(np.array([[[1]],[[2]]],dtype=np.float32),np.array([[10,11],[20,21]],dtype=np.float32))
    assert_array_equal(y,[[[1,10,11]],[[2,20,21]]]);assert y.dtype==np.float32


def empty(m):
    for shape,g in [((0,3,2),(0,4)),((2,0,2),(2,4))]:
        y=m.concat_local_global(np.empty(shape),np.empty(g));assert y.shape==(shape[0],shape[1],6)


def permutation(m):
    rng=np.random.default_rng(20261113)
    x=rng.normal(size=(4,19,7));g=rng.normal(size=(4,11));order=rng.permutation(19)
    a=m.concat_local_global(x,g)
    assert_array_equal(m.concat_local_global(x[:,order],g),a[:,order])
    assert_array_equal(a[:,:,:7],x)
    for b in range(4):
        for n in range(19):assert_array_equal(a[b,n,7:],g[b])


def storage(m):
    x=np.arange(24,dtype=float).reshape(2,3,4)[:,:,::-1];g=np.arange(12,dtype=float).reshape(2,6)[:,::2]
    old=x.copy();prior=g.copy();y=m.concat_local_global(x,g)
    assert not np.shares_memory(y,x) and not np.shares_memory(y,g)
    assert_array_equal(x,old);assert_array_equal(g,prior)


def invalid(m):
    with np.testing.assert_raises(TypeError):m.concat_local_global([],np.ones((1,1)))
    for x,g in [(np.ones((1,2)),np.ones((1,1))),(np.ones((1,2,3)),np.ones((2,1))),(np.ones((1,2,3)),np.ones((1,1),dtype=np.float32)),(np.empty((1,2,0)),np.ones((1,1))),(np.full((1,2,3),np.nan),np.ones((1,1))),(np.ones((1,2,3)),np.empty((1,0)))]:
        with np.testing.assert_raises(ValueError):m.concat_local_global(x,g)


def scale(m):
    x=np.zeros((8,256,32),dtype=np.float32);g=np.ones((8,64),dtype=np.float32)
    y=m.concat_local_global(x,g);assert y.shape==(8,256,96)
    assert_array_equal(y[:,:,32:],np.ones((8,256,64)))


TESTS=[("Append shared context","public",one_cloud),("Separate cloud context","public",two_clouds),("Empty axes","public",empty),
       ("Point permutation equivariance","hidden",permutation),("Independent noncontiguous storage","hidden",storage),
       ("Validation","hidden",invalid),("Realistic cloud batch","hidden",scale)]
