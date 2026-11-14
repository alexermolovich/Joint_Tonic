import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def fixture():return [np.array([[0.,0,2]]),np.zeros((1,3)),np.array([[0.,0,1]]),np.array([[0.,1,0]]),np.zeros((1,3)),np.array([[2.,0,0]]),np.eye(4)]
def first(m):
 r=m.scan_residuals(*fixture());assert_array_equal(r['plane'],[2]);assert_array_equal(r['line'],[1])
def sign(m):
 a=fixture();a[2]*=-1;a[4],a[5]=a[5],a[4];r=m.scan_residuals(*a);assert_array_equal(r['plane'],[-2]);assert_array_equal(r['line'],[1])
def oracle(m):
 rng=np.random.default_rng(823);p=rng.normal(size=(8192,6))[:,::2];q=rng.normal(size=(8192,3));n=rng.normal(size=(8192,3));n/=np.linalg.norm(n,axis=1,keepdims=True);a=rng.normal(size=(8192,3));b=a+np.array([1.,2.,3.]);t=np.eye(4);t[:3,:3]=rz(.7);t[:3,3]=[1.,-.5,.2];before=p.copy();r=m.scan_residuals(p,q,n,p,a,b,t)
 indices=np.arange(0,8192,37);planes=[];lines=[]
 for i in indices:
  point=np.array([sum(t[j,k]*float(p[i,k]) for k in range(3))+t[j,3] for j in range(3)]);planes.append(sum(n[i,j]*(point[j]-q[i,j]) for j in range(3)))
  axis=b[i]-a[i];delta=point-a[i];projection=delta-axis*np.dot(delta,axis)/np.dot(axis,axis);lines.append(np.sqrt(np.dot(projection,projection)))
 assert_allclose(r['plane'][indices],planes,atol=1e-12);assert_allclose(r['line'][indices],lines,atol=1e-12);assert_array_equal(p,before);assert not np.shares_memory(r['plane'],p)
def empty(m):
 z=np.empty((0,3));r=m.scan_residuals(z,z,z,z,z,z,np.eye(4));assert r['plane'].shape==r['line'].shape==(0,)
 a=fixture();a[2]*=1+5e-10;assert_allclose(m.scan_residuals(*a)['plane'],[2],atol=1e-12)
def invalid(m):
 for index,value in [(2,np.zeros((1,3))),(5,np.zeros((1,3))),(6,np.zeros((4,4))),(0,np.zeros((1,2)))]:
  a=fixture();a[index]=value;bad(lambda:m.scan_residuals(*a))
TESTS=[('Plane and line distances','public',first),('Orientation conventions','public',sign),('Independent projection oracle at scan scale','hidden',oracle),('Empty features and normal normalization','hidden',empty),('Invalid geometry','hidden',invalid)]
