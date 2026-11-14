import numpy as np
from numpy.testing import assert_allclose,assert_array_equal


def three_bins(m):assert_allclose(m.stratified_samples(np.array([1.]),np.array([4.]),np.array([[0.,.5,.75]])),[[1,2.5,3.75]],atol=1e-9)


def independent_bounds(m):assert_allclose(m.stratified_samples(np.array([0.,2.]),np.array([2.,6.]),np.array([[.25,.75],[.5,0.]])),[[.25,1.75],[3,4]],atol=1e-9)


def singleton(m):assert_allclose(m.stratified_samples(np.array([2.]),np.array([6.]),np.array([[.25]])),[[3]],atol=1e-9)


def bin_oracle(m):
    rng=np.random.default_rng(20261113);near=rng.uniform(0,10,33);far=near+rng.uniform(1,20,33);u=rng.uniform(size=(33,19))[:,::-1]
    old=[x.copy() for x in (near,far,u)]
    result=m.stratified_samples(near,far,u)
    expected=np.array([[near[r]+(i+u[r,i])*(far[r]-near[r])/19 for i in range(19)] for r in range(33)])
    assert_allclose(result,expected,atol=1e-9,rtol=1e-7)
    assert np.all(np.diff(result,axis=1)>=0)
    for x,y in zip((near,far,u),old):assert_array_equal(x,y);assert not np.shares_memory(x,result)


def no_random(m):
    old=np.random.random
    def forbidden(*args,**kwargs):raise AssertionError("Must use supplied draws")
    np.random.random=forbidden
    try:assert_allclose(m.stratified_samples(np.array([0.]),np.array([1.]),np.array([[.5]])),[[.5]])
    finally:np.random.random=old


def invalid(m):
    with np.testing.assert_raises(TypeError):m.stratified_samples([0.],np.array([1.]),np.array([[.5]]))
    for a,b,u in [(np.array([0.]),np.array([0.]),np.array([[.5]])),(np.array([0.]),np.array([1.]),np.array([[1.]])),(np.array([0.]),np.array([1.]),np.empty((1,0))),(np.array([0.],dtype=np.float32),np.array([1.]),np.array([[.5]])),(np.array([0.]),np.array([1.]),np.array([[np.nan]])),(np.array([0.]),np.array([1e7]),np.array([[.5]]))]:
        with np.testing.assert_raises(ValueError):m.stratified_samples(a,b,u)


TESTS=[("Three metric bins","public",three_bins),("Different ray bounds","public",independent_bounds),("One bin","public",singleton),
       ("Independent scalar bin oracle","hidden",bin_oracle),("Supplied randomness only","hidden",no_random),("Validation","hidden",invalid)]
