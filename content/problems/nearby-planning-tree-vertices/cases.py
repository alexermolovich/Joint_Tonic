import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def first(m):
 ids,dist=m.nearby_vertices(np.array([[0.,0.],[1.,0.],[0.,2.]]),np.zeros(2),np.array([4.,1.]),2);assert_array_equal(ids,[0,1,2]);assert_array_equal(dist,[0,2,2])
def duplicates(m):
 ids,dist=m.nearby_vertices(np.array([[1.],[0.],[0.]]),np.zeros(1),np.ones(1),0);assert_array_equal(ids,[1,2]);assert_array_equal(dist,[0,0])
def oracle(m):
 v=np.array([[3.,0.],[1.,1.],[-1.,2.],[0.,0.]]);q=np.array([.2,.3]);w=np.array([2.,.5]);ds=[sum(w[j]*(p[j]-q[j])**2 for j in range(2)) for p in v];ids,dist=m.nearby_vertices(v,q,w,2);wanted=[i for i,x in enumerate(ds) if x<=4];assert_array_equal(ids,wanted);assert_allclose(dist,[ds[i]**.5 for i in wanted]);ids,dist=m.nearby_vertices(np.empty((0,2)),q,w,1);assert ids.shape==dist.shape==(0,)
def scale(m):
 v=np.zeros((100000,6))[:,::2];before=v.copy();ids,dist=m.nearby_vertices(v,np.zeros(3),np.ones(3),0);assert_array_equal(ids,np.arange(100000));assert not dist.any();assert_array_equal(v,before);assert not np.shares_memory(dist,v)
def invalid(m):
 for w,r in [(np.zeros(1),1),(np.ones(1),-1),(np.ones(1),True),(np.ones(1),10**1000)]:
  with np.testing.assert_raises(ValueError):m.nearby_vertices(np.zeros((1,1)),np.zeros(1),w,r)
TESTS=[('Weighted inclusive radius','public',first),('Zero radius duplicates','public',duplicates),('Scalar metric and empty tree','hidden',oracle),('Large noncontiguous tree','hidden',scale),('Invalid metric contract','hidden',invalid)]
