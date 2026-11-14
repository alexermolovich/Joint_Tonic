import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def zero(m):
 r=m.gp_motion_factor(np.zeros((1,2)),np.zeros((1,2)),1,np.ones(1));assert_array_equal(r['residual'],[[0,0]]);assert_array_equal(r['whitened'],[[0,0]]);assert r['cost']==0;assert_allclose(r['covariance'],[[[1/3,.5],[.5,1]]])
def displaced(m):
 r=m.gp_motion_factor(np.zeros((1,2)),np.array([[1.,0]]),1,np.ones(1));assert_allclose(r['whitened'],[[np.sqrt(3),-3]]);assert_allclose(r['cost'],6)
def oracle(m):
 rng=np.random.default_rng(813);a=rng.normal(size=(16,4))[:,::2];b=rng.normal(size=(16,4))[:,::2];c=np.linspace(.1,4,16);before=[a.copy(),b.copy(),c.copy()]
 for t in [.001,.7,100]:
  r=m.gp_motion_factor(a,b,t,c);total=0
  for d in range(16):
   e0=b[d,0]-a[d,0]-t*a[d,1];e1=b[d,1]-a[d,1]
   total+=.5*(12*e0*e0/t**3-12*e0*e1/t**2+4*e1*e1/t)/c[d]
   assert_allclose(np.linalg.cholesky(r['covariance'][d])@r['whitened'][d],[e0,e1],rtol=1e-10,atol=1e-10)
  assert_allclose(r['cost'],total,rtol=1e-10)
 for x,y in zip(before,[a,b,c]):assert_array_equal(x,y)
 assert not np.shares_memory(r['residual'],b)
def deterministic(m):
 a=np.array([[2.,3.]]);b=np.array([[8.,3.]]);r=m.gp_motion_factor(a,b,2,np.array([.5]));assert_array_equal(r['whitened'],[[0,0]])
def invalid(m):
 for t in [0,1e-4,101,True,10**1000]:bad(lambda:m.gp_motion_factor(np.zeros((1,2)),np.zeros((1,2)),t,np.ones(1)))
 bad(lambda:m.gp_motion_factor(np.zeros((1,2)),np.zeros((1,2)),1,np.zeros(1)))
 bad(lambda:m.gp_motion_factor(np.zeros((1,2)),np.zeros((2,2)),1,np.ones(1)))
 bad(lambda:m.gp_motion_factor(np.zeros((0,2)),np.zeros((0,2)),1,np.ones(0)))
 bad(lambda:m.gp_motion_factor(np.zeros((1,2),dtype=np.float32),np.zeros((1,2)),1,np.ones(1)))
TESTS=[('Zero state residual','public',zero),('Coupled whitening','public',displaced),('Independent inverse-covariance oracle and scale','hidden',oracle),('Constant-velocity agreement','hidden',deterministic),('Invalid physical contract','hidden',invalid)]
