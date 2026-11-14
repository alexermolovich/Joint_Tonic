import numpy as np
from numpy.testing import assert_allclose,assert_array_equal


def data():return np.array([[[[[2.,4.]],[[10.,20.]]]]]),np.array([[[[1.],[3.]]]])


def missing_view(m):
    f,w=data();y,v=m.aggregate_camera_features(f,w,np.array([[[[True],[False]]]]))
    assert_allclose(y,[[[2,4]]]);assert_array_equal(v,[[True]])


def fuse(m):
    f,w=data();y,v=m.aggregate_camera_features(f,w,np.ones_like(w,dtype=bool))
    assert_allclose(y,[[[8,16]]]);assert_array_equal(v,[[True]])


def no_mass(m):
    f,w=data();y,v=m.aggregate_camera_features(f,w*0,np.ones_like(w,dtype=bool))
    assert_array_equal(y,np.zeros((1,1,2)));assert_array_equal(v,[[False]])


def tiny_mass(m):
    f=np.array([[[[[1e-6,-2e-6]]]]]);w=np.array([[[[1e-320]]]])
    y,v=m.aggregate_camera_features(f,w,np.ones_like(w,dtype=bool))
    assert_allclose(y,[[[1e-6,-2e-6]]],rtol=1e-7,atol=1e-12);assert_array_equal(v,[[True]])


def oracle(m):
    rng=np.random.default_rng(20261113);f=rng.normal(size=(3,7,4,5,9));w=rng.uniform(size=(3,7,4,5));v=rng.random((3,7,4,5))>.3;old=[x.copy() for x in (f,w,v)]
    y,o=m.aggregate_camera_features(f,w,v)
    for b in range(3):
        for q in range(7):
            values=[(w[b,q,c,s],f[b,q,c,s]) for c in range(4) for s in range(5) if v[b,q,c,s]]
            expected=sum((mass*feature for mass,feature in values),start=np.zeros(9))/sum(mass for mass,_ in values)
            assert_allclose(y[b,q],expected,atol=1e-9)
    for x,z in zip((f,w,v),old):assert_array_equal(x,z);assert not np.shares_memory(y,x)
    assert o.all()


def invalid(m):
    f,w=data();v=np.ones_like(w,dtype=bool)
    with np.testing.assert_raises(TypeError):m.aggregate_camera_features([],w,v)
    for a,b,c in [(f.astype(np.float32),w,v),(f,w* -1,v),(f,w,v.astype(int)),(f,w[:,:,:,0],v),(np.full_like(f,np.inf),w,np.zeros_like(v))]:
        with np.testing.assert_raises(ValueError):m.aggregate_camera_features(a,b,c)


TESTS=[("Unavailable camera excluded","public",missing_view),("Two-view weighted mean","public",fuse),("No positive evidence","public",no_mass),
       ("Subnormal positive weight","hidden",tiny_mass),("Independent masked reduction oracle","hidden",oracle),("Validation","hidden",invalid)]
