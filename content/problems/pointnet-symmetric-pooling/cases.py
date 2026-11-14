import numpy as np
from numpy.testing import assert_array_equal


def permutation(m):
    x=np.array([[[1.,-2.],[3.,-4.],[2.,-1.]]])
    assert_array_equal(m.symmetric_point_pool(x),[[3,-1]])
    assert_array_equal(m.symmetric_point_pool(x[:,[2,0,1]]),[[3,-1]])


def padding(m):
    x=np.array([[[-5.,-2.],[99.,99.],[-3.,-8.]]],dtype=np.float32)
    mask=np.array([[True,False,True]])
    y=m.symmetric_point_pool(x,mask)
    assert_array_equal(y,[[-3,-2]])
    assert y.dtype==np.float32


def singleton(m):
    x=np.array([[[-7.]]])
    assert_array_equal(m.symmetric_point_pool(x),[[-7.]])


def randomized(m):
    rng=np.random.default_rng(20261113)
    x=rng.normal(size=(7,101,13));mask=rng.random((7,101))>.3
    expected=np.stack([np.max(cloud[valid],axis=0) for cloud,valid in zip(x,mask)])
    permutation=rng.permutation(101)
    assert_array_equal(m.symmetric_point_pool(x,mask),expected)
    assert_array_equal(m.symmetric_point_pool(x[:,permutation],mask[:,permutation]),expected)
    assert_array_equal(m.symmetric_point_pool(x[:,::-1],mask[:,::-1]),expected)


def duplicates(m):
    x=np.array([[[4.,-2.],[4.,-2.],[1.,-3.]],[[2.,9.],[2.,9.],[-1.,5.]]])
    assert_array_equal(m.symmetric_point_pool(x),[[4,-2],[2,9]])


def ownership(m):
    x=np.arange(24,dtype=np.float64).reshape(2,3,4);old=x.copy()
    mask=np.ones((2,3),dtype=bool);prior=mask.copy()
    out=m.symmetric_point_pool(x,mask)
    assert not np.shares_memory(x,out)
    assert_array_equal(x,old);assert_array_equal(mask,prior)


def invalid(m):
    with np.testing.assert_raises(TypeError):m.symmetric_point_pool([[[1.]]])
    with np.testing.assert_raises(TypeError):m.symmetric_point_pool(np.ones((1,1,1)),[[True]])
    for x,mask in [(np.ones((1,2,3),dtype=int),None),(np.ones((1,2)),None),(np.empty((1,0,3)),None),(np.full((1,2,3),np.nan),None),(np.ones((1,2,3)),np.zeros((1,2),dtype=bool)),(np.ones((1,2,3)),np.ones((1,2))), (np.ones((1,2,3)),np.ones((2,1),dtype=bool))]:
        with np.testing.assert_raises(ValueError):m.symmetric_point_pool(x,mask)
    x=np.ones((1,2,1));x[0,1,0]=np.inf
    with np.testing.assert_raises(ValueError):m.symmetric_point_pool(x,np.array([[True,False]]))


def scale(m):
    x=np.arange(8*1024*32,dtype=np.float32).reshape(8,1024,32)
    assert_array_equal(m.symmetric_point_pool(x),x[:,-1,:])


TESTS=[("Point permutation","public",permutation),("Negative-value padding","public",padding),("Single point","public",singleton),
       ("Batched joint permutation","hidden",randomized),("Duplicates and ties","hidden",duplicates),
       ("Input preservation","hidden",ownership),("Validation","hidden",invalid),("Realistic clouds","hidden",scale)]
