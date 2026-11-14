import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def args():return [np.array([[1.,0.]]),np.array([.5]),np.array([2.,2,0,0]),np.array([2.,2,0,0]),np.eye(4),np.array([4,4],dtype=np.int64)]
def first(m):
 r=m.warp_pixels(*args());assert_array_equal(r['target_points'],[[1,0,2]]);assert_array_equal(r['target_pixels'],[[1,0]]);assert r['visible'][0]
def second(m):
 a=args();a[4][0,3]=1;r=m.warp_pixels(*a);assert_array_equal(r['target_points'],[[2,0,2]]);assert_array_equal(r['target_pixels'],[[2,0]])
def boundaries(m):
 a=args();a[0]=np.array([[0.,0.],[4.,0.],[-1.,0.]]);a[1]=np.ones(3);r=m.warp_pixels(*a);assert_array_equal(r['visible'],[True,False,False]);assert_allclose(r['target_pixels'],a[0])
 a=args();a[4][2,3]=-2;r=m.warp_pixels(*a);assert not r['visible'][0] and np.isnan(r['target_pixels']).all()
 a=args();a[0]=np.empty((0,2));a[1]=np.empty(0);assert m.warp_pixels(*a)['target_points'].shape==(0,3)
def oracle(m):
 rng=np.random.default_rng(821);uv=rng.uniform(-2,2,(16384,4))[:,::2];rho=rng.uniform(.2,2,16384);src=np.array([2.,3,.1,.2]);dst=np.array([3.,4,2,1]);t=np.eye(4);t[:3,:3]=rz(.7);t[:3,3]=[.1,-.2,.3];before=[uv.copy(),rho.copy(),t.copy()];r=m.warp_pixels(uv,rho,src,dst,t,np.array([16,16],dtype=np.int64))
 expected=[]
 for i in range(0,len(uv),61):
  p=[(float(uv[i,0])-.1)/2/rho[i],(float(uv[i,1])-.2)/3/rho[i],1/rho[i]];q=[sum(t[j,k]*p[k] for k in range(3))+t[j,3] for j in range(3)];expected.append([3*q[0]/q[2]+2,4*q[1]/q[2]+1])
 assert_allclose(r['target_pixels'][::61],expected,atol=1e-12)
 for a,b in zip(before,[uv,rho,t]):assert_array_equal(a,b)
 assert not np.shares_memory(r['target_points'],uv)
def invalid(m):
 for index,value in [(1,np.array([0.])),(2,np.array([0.,1,0,0])),(4,np.zeros((4,4))),(5,np.array([0,4],dtype=np.int64))]:
  a=args();a[index]=value;bad(lambda:m.warp_pixels(*a))
TESTS=[('Identity calibrated warp','public',first),('Transform direction','public',second),('Depth and image boundaries','hidden',boundaries),('Rotated scalar projection oracle at scale','hidden',oracle),('Invalid calibration','hidden',invalid)]
