import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def matrix_exp(xi):
 x,y,z=xi[3:];hat=np.zeros((4,4));hat[:3,:3]=[[0,-z,y],[z,0,-x],[-y,x,0]];hat[:3,3]=xi[:3];out=np.eye(4);term=np.eye(4)
 for k in range(1,61):term=term@hat/k;out+=term
 return out
def translation(m):
 r=m.se3_maps(np.array([1.,0,0,0,0,0]),np.eye(4));expected=np.eye(4);expected[0,3]=1;assert_array_equal(r['exponential'],expected);assert_array_equal(r['logarithm'],np.zeros(6))
def coupled(m):
 xi=np.array([1.,0,0,0,0,np.pi/2]);t=np.eye(4);t[:3,:3]=rz(np.pi/2);t[:3,3]=[2/np.pi,2/np.pi,0];r=m.se3_maps(xi,t);assert_allclose(r['exponential'],t,atol=1e-12);assert_allclose(r['logarithm'],xi,atol=1e-12)
def oracle(m):
 rng=np.random.default_rng(826)
 for angle in [0.,1e-12,1e-7,1e-4,.7,2.4,np.pi-1.01e-4]:
  axis=rng.normal(size=3);axis/=np.linalg.norm(axis);xi=np.r_[rng.normal(size=3),angle*axis];t=matrix_exp(xi);before=[xi.copy(),t.copy()];r=m.se3_maps(xi,t)
  assert_allclose(r['exponential'],t,rtol=1e-10,atol=1e-11);assert_allclose(r['logarithm'],xi,rtol=1e-7,atol=1e-9)
  assert_array_equal(xi,before[0]);assert_array_equal(t,before[1]);assert not np.shares_memory(r['exponential'],t)
def independent(m):
 storage=np.zeros(12);xi=storage[::2];xi[0]=2;t=np.eye(4);t[1,3]=3;r=m.se3_maps(xi,t);assert_array_equal(r['logarithm'],[0,3,0,0,0,0]);assert r['exponential'][0,3]==2
def invalid(m):
 for xi,t in [(np.array([0.,0,0,np.pi,0,0]),np.eye(4)),(np.zeros(6),np.diag([-1.,-1,1,1])),(np.zeros(6),np.zeros((4,4))),(np.ones(6)*1e6,np.eye(4)),(np.zeros(5),np.eye(4))]:bad(lambda:m.se3_maps(xi,t))
TESTS=[('Pure translation and identity log','public',translation),('Coupled screw increment','public',coupled),('Independent matrix-series oracle across angles','hidden',oracle),('Independent inputs and strided tangent','hidden',independent),('Invalid transform and branch','hidden',invalid)]
