import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def args():return [np.array([[0.,0.,1.]]),np.array([[1.,0.]]),np.eye(4)[None],np.array([1.,1.,0.,0.]),np.ones(1),np.ones(1,bool),1.]
def one(m):
 r=m.pose_inliers(*args());assert_allclose(r['squared_error'],[[1]]);assert_array_equal(r['counts'],[1]);assert r['best']==0
def compare(m):
 a=args();a[2]=np.tile(np.eye(4),(2,1,1));a[2][1,0,3]=1;r=m.pose_inliers(*a);assert_allclose(r['squared_error'],[[1],[0]]);assert r['best']==1
def oracle(m):
 rng=np.random.default_rng(847);p=rng.normal(size=(2048,6))[:,::2];p[:,2]+=4;uv=rng.normal(size=(2048,4))[:,::2];t=np.tile(np.eye(4),(8,1,1));t[:,:3,3]=rng.normal(scale=.2,size=(8,3));t[2,:3,:3]=np.array([[0.,-1,0],[1,0,0],[0,0,1.]]);std=rng.uniform(.5,2,2048);mask=rng.random(2048)>.2;before=p.copy();r=m.pose_inliers(p,uv,t,np.array([2.,3.,.1,.2]),std,mask,4);errors=np.full((8,2048),np.inf)
 for i in range(8):
  for j in range(2048):
   q=t[i,:3,:3]@p[j]+t[i,:3,3]
   if mask[j] and q[2]>1e-6:prediction=np.array([2*q[0]/q[2]+.1,3*q[1]/q[2]+.2]);errors[i,j]=sum((prediction-uv[j])**2)/std[j]**2
 expected=errors<=4;counts=expected.sum(axis=1);median=np.array([np.median(errors[i,expected[i]]) for i in range(8)]);assert_allclose(r['squared_error'],errors);assert_array_equal(r['inliers'],expected);assert_array_equal(r['counts'],counts);assert_allclose(r['median_error'],median);assert r['best']==min(range(8),key=lambda i:(-counts[i],median[i],i));assert_array_equal(p,before);assert not np.shares_memory(r['squared_error'],p)
def edges(m):
 a=args();a[0][0,2]=1e-6;r=m.pose_inliers(*a);assert r['best']==-1 and np.isinf(r['squared_error']).all() and np.isnan(r['median_error']).all()
 a=args();a[4][0]=2;r=m.pose_inliers(*a);assert_allclose(r['squared_error'],[[.25]])
 a=args();a[0]=np.empty((0,3));a[1]=np.empty((0,2));a[4]=np.empty(0);a[5]=np.empty(0,bool);r=m.pose_inliers(*a);assert r['best']==-1 and r['inliers'].shape==(1,0)
def invalid(m):
 a=args();a[6]=10**1000;bad(lambda:m.pose_inliers(*a));a=args();a[4][0]=0;bad(lambda:m.pose_inliers(*a));a=args();a[2][0,0,0]=2;bad(lambda:m.pose_inliers(*a))
TESTS=[('Inclusive squared error threshold','public',one),('Median tie break across pose hypotheses','public',compare),('Scalar calibrated geometric oracle at scale','hidden',oracle),('Depth cutoff uncertainty and no evidence','hidden',edges),('Invalid camera uncertainties and scalars','hidden',invalid)]
