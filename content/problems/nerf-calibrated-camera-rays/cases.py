import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def example(m):
    o,d=m.camera_rays(np.array([[0.,0.],[1.,0.]]),np.eye(3),np.eye(4));assert_allclose(o,0);assert_allclose(d,[[0,0,1],[2**-.5,0,2**-.5]])
def translated(m):
    k=np.array([[2.,0,1],[0,2,1],[0,0,1]]);t=np.eye(4);t[:3,3]=[3,0,2]
    o,d=m.camera_rays(np.array([[1.,1.]]),k,t);assert_allclose(o,[[3,0,2]]);assert_allclose(d,[[0,0,1]])
def rotation(m):
    t=np.eye(4);t[:3,:3]=[[0,0,1],[0,1,0],[-1,0,0]]
    o,d=m.camera_rays(np.array([[0.,0.],[0.,1.]]),np.eye(3),t);assert_allclose(d,[[1,0,0],[2**-.5,2**-.5,0]])
    r=np.random.default_rng(7);p=r.uniform(-10,10,(303,2));o,d=m.camera_rays(p,np.eye(3),t)
    expected=np.array([[1,v,-u]/np.linalg.norm([u,v,1]) for u,v in p]);assert_allclose(d,expected)
def empty(m):
    o,d=m.camera_rays(np.empty((0,2)),np.eye(3),np.eye(4));assert o.shape==d.shape==(0,3)
def invalid(m):
    p=np.zeros((1,2));k=np.eye(3);t=np.eye(4)
    bad=t.copy();bad[0,0]=-1
    for args in [(p,k,bad),(p,k*2,t),(p.astype(np.float32),k,t),(np.array([[np.inf,0]]),k,t)]:
        with np.testing.assert_raises(ValueError):m.camera_rays(*args)
def storage(m):
    p=np.arange(8.).reshape(2,4)[:,::2];k=np.eye(3);t=np.eye(4);copies=[x.copy() for x in (p,k,t)]
    o,d=m.camera_rays(p,k,t)
    for x,c in zip((p,k,t),copies):
        assert_array_equal(x,c);assert not np.shares_memory(o,x);assert not np.shares_memory(d,x)
TESTS=[('Identity rays','public',example),('Translated center','public',translated),('Rotated scalar oracle','hidden',rotation),('Empty pixels','hidden',empty),('Validation','hidden',invalid),('Storage','hidden',storage)]
