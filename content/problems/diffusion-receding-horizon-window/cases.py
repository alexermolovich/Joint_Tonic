import numpy as np
from numpy.testing import assert_array_equal


def window(m):
    p=np.array([[[10.],[20.],[30.],[40.]]])
    out=m.receding_horizon_window(p,np.ones((1,4),dtype=bool),1,2)
    assert_array_equal(out,[[[20],[30]]])
    assert out.dtype==p.dtype


def padded_tail(m):
    p=np.array([[[1.,2.],[3.,4.],[0.,0.]]],dtype=np.float32);v=np.array([[True,True,False]])
    out=m.receding_horizon_window(p,v,0,2)
    assert_array_equal(out,[[[1,2],[3,4]]]);assert out.dtype==np.float32
    with np.testing.assert_raises(ValueError):m.receding_horizon_window(p,v,1,2)


def boundaries(m):
    p=np.arange(12.,dtype=np.float64).reshape(2,3,2);v=np.ones((2,3),dtype=bool)
    assert_array_equal(m.receding_horizon_window(p,v,0,3),p)
    assert_array_equal(m.receding_horizon_window(p,v,2,1),p[:,2:])
    v[1,1]=False
    with np.testing.assert_raises(ValueError):m.receding_horizon_window(p,v,0,2)
    assert_array_equal(m.receding_horizon_window(p,v,2,1),p[:,2:])


def storage_and_scale(m):
    p=np.arange(16*64*8.,dtype=np.float32).reshape(16,64,8)[:,:,::2]
    v=np.ones((64,16),dtype=bool).T;before=p.copy()
    out=m.receding_horizon_window(p,v,7,12)
    assert_array_equal(out,before[:,7:19]);assert not np.shares_memory(out,p)
    out[:]=-1;assert_array_equal(p,before)


def contracts(m):
    p=np.zeros((1,3,2));v=np.ones((1,3),dtype=bool)
    for pp,vv in [(p.tolist(),v),(p,v.tolist())]:
        with np.testing.assert_raises(TypeError):m.receding_horizon_window(pp,vv,0,1)
    for off,count in [(True,1),(0,False),(0.,1),(0,np.int64(1))]:
        with np.testing.assert_raises(TypeError):m.receding_horizon_window(p,v,off,count)
    for off,count in [(-1,1),(3,1),(0,0),(2,2),(0,4)]:
        with np.testing.assert_raises(ValueError):m.receding_horizon_window(p,v,off,count)
    for bad in (p.astype(int),p[0],p[:,:0],np.full_like(p,np.nan),np.full_like(p,1e6+1)):
        with np.testing.assert_raises(ValueError):m.receding_horizon_window(bad,v,0,1)
    with np.testing.assert_raises(ValueError):m.receding_horizon_window(p,v.astype(int),0,1)


TESTS=[("Aligned near-term window","public",window),("Unselected padding versus selected padding","public",padded_tail),
       ("Boundary windows and batch rejection","hidden",boundaries),("Fresh noncontiguous buffer at scale","hidden",storage_and_scale),
       ("Typed bounded contract","hidden",contracts)]
