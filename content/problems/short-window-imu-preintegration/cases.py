import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def one(m):
 r=m.preintegrate_window(np.zeros((1,3)),np.array([[2.,0.,0.]]),np.zeros(3),np.zeros(3),np.array([.1]));assert_allclose(r['velocity'][-1],[.2,0,0]);assert_allclose(r['position'][-1],[.01,0,0]);assert_allclose(r['rotations'][-1],np.eye(3))
def turning(m):
 r=m.preintegrate_window(np.tile([0.,0.,np.pi/2],(2,1)),np.tile([1.,0.,0.],(2,1)),np.zeros(3),np.zeros(3),np.ones(2));assert_allclose(r['rotations'][-1],np.diag([-1,-1,1]),atol=1e-12);assert_allclose(r['velocity'][-1],[1,1,0]);assert_allclose(r['position'][-1],[1.5,.5,0])
def oracle(m):
 rng=np.random.default_rng(843);n=512;w=rng.normal(size=(n,6))[:,::2];f=rng.normal(size=(n,6))[:,::2];dt=rng.uniform(.001,.01,n);bg=np.array([.1,-.2,.3]);ba=np.array([.2,.1,-.1]);before=f.copy();out=m.preintegrate_window(w,f,bg,ba,dt);r=np.eye(3);v=np.zeros(3);p=np.zeros(3)
 for k in range(n):
  # Independent matrix-exponential power series, not Rodrigues.
  x,y,z=(w[k]-bg)*dt[k];generator=np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]]);term=np.eye(3);inc=term.copy()
  for order in range(1,18):term=term@generator/order;inc+=term
  force=r@(f[k]-ba);p=p+v*dt[k]+force*dt[k]**2/2;v=v+force*dt[k];r=r@inc;assert_allclose(out['rotations'][k+1],r,atol=1e-12);assert_allclose(out['velocity'][k+1],v,atol=1e-12);assert_allclose(out['position'][k+1],p,atol=1e-12)
 assert_array_equal(f,before);assert not np.shares_memory(out['position'],f);assert_allclose(out['elapsed'],np.r_[0,dt.cumsum()])
def edges(m):
 r=m.preintegrate_window(np.empty((0,3)),np.empty((0,3)),np.zeros(3),np.zeros(3),np.empty(0));assert_array_equal(r['rotations'],np.eye(3)[None]);assert r['velocity'].shape==(1,3)
 bias=np.array([1.,2.,3.]);r=m.preintegrate_window(bias[None],bias[None],bias,bias,np.array([1.]));assert_array_equal(r['velocity'],np.zeros((2,3)))
 r=m.preintegrate_window(np.array([[1e-12,0.,0.]]),np.zeros((1,3)),np.zeros(3),np.zeros(3),np.ones(1));assert_allclose(r['rotations'][-1,2,1],1e-12,atol=1e-25)
def invalid(m):
 for w,dt in [(np.ones((1,3),np.float32),np.ones(1)),(np.ones((1,3)),np.zeros(1)),(np.ones((1,3))*101,np.ones(1)),(np.ones((101,3)),np.ones(101))]:bad(lambda:m.preintegrate_window(w,np.zeros(w.shape),np.zeros(3),np.zeros(3),dt))
TESTS=[('One specific-force interval','public',one),('Coupled rotation and translation','public',turning),('Independent matrix-series recurrence at scale','hidden',oracle),('Empty bias cancellation and small angles','hidden',edges),('Invalid IMU sample contract','hidden',invalid)]
