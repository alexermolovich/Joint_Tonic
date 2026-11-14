import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def fixture():return [np.eye(3),np.array([1.,2,3]),np.array([4.,5,6]),np.zeros((5,3,3)),np.array([0.,0,.01]),np.array([.01,0,0])]
def zero(m):
 a=fixture();r=m.correct_preintegration(*a)
 for key,x in zip(['rotation','velocity','position'],a[:3]):assert_array_equal(r[key],x);assert not np.shares_memory(r[key],x)
def second(m):
 a=fixture();a[1]=np.zeros(3);a[2]=np.zeros(3);a[3][0]=np.eye(3);a[3][2]=2*np.eye(3);a[3][4]=.5*np.eye(3);r=m.correct_preintegration(*a);assert_allclose(r['rotation'],rz(.01),atol=1e-12);assert_allclose(r['velocity'],[.02,0,0]);assert_allclose(r['position'],[.005,0,0])
def oracle(m):
 rng=np.random.default_rng(829)
 for _ in range(24):
  a=fixture();a[0]=rz(.7);store=rng.normal(size=(5,3,6));a[3]=store[:,:,::2];a[4]=rng.normal(size=3)*.001;a[5]=rng.normal(size=3)*.001;before=[x.copy() for x in a];r=m.correct_preintegration(*a)
  for key,base,gidx,aidx in [('velocity',a[1],1,2),('position',a[2],3,4)]:
   expected=[base[i]+sum(a[3][gidx,i,k]*a[4][k]+a[3][aidx,i,k]*a[5][k] for k in range(3)) for i in range(3)];assert_allclose(r[key],expected,atol=1e-12)
  phi=a[3][0]@a[4];theta=np.linalg.norm(phi);axis=phi/theta;half=theta/2;w=np.cos(half);x,y,z=axis*np.sin(half);quatrot=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]]);assert_allclose(r['rotation'],a[0]@quatrot,atol=1e-12)
  for x,y in zip(before,a):assert_array_equal(x,y)
def right_update(m):
 a=fixture();a[0]=rz(np.pi/2);a[3][0]=np.eye(3);a[4]=np.array([.01,0,0]);r=m.correct_preintegration(*a);rx=np.array([[1.,0,0],[0,np.cos(.01),-np.sin(.01)],[0,np.sin(.01),np.cos(.01)]]);assert_allclose(r['rotation'],a[0]@rx,atol=1e-12);assert not np.allclose(r['rotation'],rx@a[0])
def invalid(m):
 for index,value in [(0,np.zeros((3,3))),(4,np.array([.02,0,0])),(5,np.array([np.nan,0,0])),(3,np.ones((4,3,3)))]:
  a=fixture();a[index]=value;bad(lambda:m.correct_preintegration(*a))
 a=fixture();a[3][0]=100*np.eye(3);bad(lambda:m.correct_preintegration(*a))
TESTS=[('Zero sensitivities preserve values','public',zero),('Known bias correction blocks','public',second),('Scalar and quaternion oracles with strided Jacobians','hidden',oracle),('Local right rotation correction','hidden',right_update),('Invalid bias envelope','hidden',invalid)]
