import numpy as np
from numpy.testing import assert_allclose,assert_array_equal


def args():return [np.array([[.5,.25]]),np.array([[[1.,0.,0.],[0.,1.,0.]]]),np.array([[2.,4.]]),np.array([.25]),np.array([0.,0.,1.])]


def transparent_color(m):
    c,d,v=m.render_rays(*args());assert_allclose(c,[[.5,.25,.25]]);assert_allclose(d,[8/3]);assert_array_equal(v,[True])


def background_only(m):
    a=args();a[0][:]=0;a[3][:]=1;a[4]=np.array([.2,.3,.4])
    c,d,v=m.render_rays(*a);assert_allclose(c,[[.2,.3,.4]]);assert np.isnan(d).all();assert_array_equal(v,[False])


def single_hit(m):
    c,d,v=m.render_rays(np.array([[1.]]),np.array([[[.2,.4,.6]]]),np.array([[7.]]),np.array([0.]),np.ones(3))
    assert_allclose(c,[[.2,.4,.6]]);assert_allclose(d,[7]);assert_array_equal(v,[True])


def threshold(m):
    for mass,expected in [(1e-8,False),(1.0001e-8,True)]:
        c,d,v=m.render_rays(np.array([[mass]]),np.ones((1,1,3)),np.array([[3.]]),np.array([1-mass]),np.zeros(3))
        assert_array_equal(v,[expected]);assert_allclose(c,[[mass]*3])
        if expected:assert_allclose(d,[3])
        else:assert np.isnan(d[0])


def oracle_storage(m):
    rng=np.random.default_rng(20261113);w=rng.uniform(size=(13,17));w=w/w.sum(1,keepdims=True)*.7;c=rng.uniform(size=(13,17,3));z=np.sort(rng.uniform(0,10,(13,17)),axis=1);bg=np.full(13,.3);bc=np.array([.2,.3,.4]);old=[x.copy() for x in (w,c,z,bg,bc)]
    rgb,depth,valid=m.render_rays(w,c,z,bg,bc)
    for r in range(13):
        assert_allclose(rgb[r],sum((w[r,i]*c[r,i] for i in range(17)),start=np.zeros(3))+.3*bc,atol=1e-9)
        assert_allclose(depth[r],sum(w[r,i]*z[r,i] for i in range(17))/.7,atol=1e-9)
    for x,y in zip((w,c,z,bg,bc),old):assert_array_equal(x,y);assert not np.shares_memory(rgb,x) and not np.shares_memory(depth,x)
    assert valid.dtype==np.bool_


def invalid(m):
    a=args();a[0]=[[.5,.25]]
    with np.testing.assert_raises(TypeError):m.render_rays(*a)
    for i,bad in [(0,np.array([[.9,.9]])),(1,np.ones((1,2,2))),(2,np.array([[4.,2.]])),(3,np.array([np.nan])),(4,np.array([2.,0.,0.]))]:
        a=args();a[i]=bad
        with np.testing.assert_raises(ValueError):m.render_rays(*a)


TESTS=[("Partial foreground color and depth","public",transparent_color),("Background without depth","public",background_only),("Single foreground hit","public",single_hit),
       ("Depth validity threshold","hidden",threshold),("Independent compositing oracle","hidden",oracle_storage),("Validation","hidden",invalid)]
