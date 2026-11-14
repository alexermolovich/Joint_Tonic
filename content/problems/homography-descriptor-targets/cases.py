import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def example(m):
 r=m.descriptor_targets(np.array([[0.,0.],[2.,0.]]),np.array([[0.,0.],[1.,0.]]),np.eye(3),np.ones(2,bool),np.ones(2,bool),1);assert_allclose(r['distances'],[[0,1],[2,1]]);assert_array_equal(r['correspondence'],[[True,True],[False,True]])
def masked(m):
 r=m.descriptor_targets(np.array([[0.,0.],[2.,0.]]),np.array([[0.,0.],[1.,0.]]),np.eye(3),np.array([False,True]),np.ones(2,bool),1);assert np.isnan(r['distances'][0]).all();assert not r['correspondence'][0].any();assert_allclose(r['distances'][1],[2,1])
def oracle(m):
 rng=np.random.default_rng(832);a=rng.normal(size=(256,4))[:,::2];b=rng.normal(size=(384,4))[:,::2];ma=rng.random(256)>.2;mb=rng.random(384)>.2;h=np.array([[1.1,.2,.5],[-.1,.9,.2],[.01,.02,1.]]);before=a.copy();r=m.descriptor_targets(a,b,h,ma,mb,.75);expected=np.full((256,384),np.nan)
 for i in range(256):
  v=h@np.r_[a[i],1.];p=v[:2]/v[2]
  if ma[i]:
   for j in range(384):
    if mb[j]:expected[i,j]=sum((p-b[j])**2)**.5
 assert_allclose(r['distances'],expected,equal_nan=True);assert_array_equal(r['correspondence'],expected<=.75);assert_array_equal(a,before);assert not np.shares_memory(r['distances'],a)
def boundaries(m):
 h=np.diag([2.,1.,1e-9]);r=m.descriptor_targets(np.zeros((1,2)),np.zeros((1,2)),h,np.ones(1,bool),np.ones(1,bool),0);assert np.isnan(r['distances']).all()
 h[2,2]=np.nextafter(1e-9,np.inf);r=m.descriptor_targets(np.zeros((1,2)),np.zeros((1,2)),h,np.ones(1,bool),np.ones(1,bool),0);assert r['correspondence'][0,0]
 r=m.descriptor_targets(np.empty((0,2)),np.ones((2,2)),np.eye(3),np.empty(0,bool),np.ones(2,bool),1);assert r['distances'].shape==(0,2)
def invalid(m):
 for a,h,mask,t in [(np.zeros((1,2),np.float32),np.eye(3),np.ones(1,bool),0),(np.zeros((1,2)),np.zeros((3,3)),np.ones(1,bool),0),(np.zeros((1,2)),np.eye(3),np.ones(1),0),(np.zeros((1,2)),np.eye(3),np.ones(1,bool),10**1000)]:bad(lambda:m.descriptor_targets(a,np.zeros((1,2)),h,mask,np.ones(1,bool),t))
TESTS=[('Geometric correspondence targets','public',example),('Masked source centers','public',masked),('Independent scalar projection distances at scale','hidden',oracle),('Projection cutoff and empty axis','hidden',boundaries),('Invalid geometry and masks','hidden',invalid)]
