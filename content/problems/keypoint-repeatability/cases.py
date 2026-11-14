import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def partial(m):
 r=m.keypoint_repeatability(np.array([[0.,0.],[2.,0.]]),np.zeros((1,2)),np.eye(3),np.array([3,3]),np.array([3,3]),0);assert_array_equal(r['source_correct'],[True,False]);assert_array_equal(r['target_correct'],[True]);assert_allclose(r['repeatability'],2/3)
def outside(m):
 h=np.eye(3);h[0,2]=3;r=m.keypoint_repeatability(np.zeros((1,2)),np.zeros((1,2)),h,np.array([3,3]),np.array([3,3]),0);assert np.isnan(r['repeatability']);assert not r['source_eligible'].any() and not r['target_eligible'].any()
def oracle(m):
 rng=np.random.default_rng(831);a=rng.uniform(0,30,(400,4))[:,::2];b=rng.uniform(0,30,(350,4))[:,::2];before=a.copy();h=np.array([[1.2,.1,-1],[.05,.8,2],[.001,-.002,1.]]);r=m.keypoint_repeatability(a,b,h,np.array([32,32]),np.array([32,32]),2)
 def project(p,t):
  q=t@np.r_[p,1.];return q[:2]/q[2]
 ab=np.array([project(p,h) for p in a]);ba=np.array([project(p,np.linalg.inv(h)) for p in b]);ea=np.array([all(0<=x<=31 for x in p) for p in ab]);eb=np.array([all(0<=x<=31 for x in p) for p in ba]);ca=[ea[i] and any(sum((ab[i]-q)**2)<=4 for q in b[eb]) for i in range(len(a))];cb=[eb[j] and any(sum((ba[j]-p)**2)<=4 for p in a[ea]) for j in range(len(b))]
 assert_array_equal(r['source_eligible'],ea);assert_array_equal(r['target_eligible'],eb);assert_array_equal(r['source_correct'],ca);assert_array_equal(r['target_correct'],cb);assert_allclose(r['repeatability'],(sum(ca)+sum(cb))/(sum(ea)+sum(eb)));assert_array_equal(a,before);assert not np.shares_memory(r['source_correct'],a)
def boundaries(m):
 size=np.array([1,4]);a=np.array([[0.,0.],[0.,0.]]);b=np.array([[1.,0.]]);r=m.keypoint_repeatability(a,b,np.eye(3),size,size,1);assert r['repeatability']==1
 r=m.keypoint_repeatability(np.empty((0,2)),b,np.eye(3),size,size,1);assert r['repeatability']==0
 r=m.keypoint_repeatability(np.empty((0,2)),np.empty((0,2)),np.eye(3),size,size,1);assert np.isnan(r['repeatability'])
def invalid(m):
 for a,h,t in [(np.array([[-1.,0.]]),np.eye(3),0),(np.zeros((1,2),np.float32),np.eye(3),0),(np.zeros((1,2)),np.zeros((3,3)),0),(np.zeros((1,2)),np.eye(3),10**1000)]:bad(lambda:m.keypoint_repeatability(a,np.zeros((1,2)),h,np.array([2,2]),np.array([2,2]),t))
TESTS=[('Symmetric partial repeatability','public',partial),('No shared field of view','public',outside),('Independent two-frame distance oracle at scale','hidden',oracle),('Inclusive distance duplicates empty sets','hidden',boundaries),('Malformed points matrix and threshold','hidden',invalid)]
