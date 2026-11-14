import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def one(m):
    r=m.preintegration_covariance(np.zeros((1,3)),np.zeros((1,3)),np.ones(1),np.array([[1.,1,1,4,4,4]]));p=r['covariance'][-1];assert_allclose(np.diag(p),[1,1,1,4,4,4,1,1,1]);assert_allclose(p[3:6,6:],2*np.eye(3));assert_allclose(r['final_rotation'],np.eye(3))
def empty(m):
    r=m.preintegration_covariance(np.empty((0,3)),np.empty((0,3)),np.empty(0),np.empty((0,6)));assert_array_equal(r['covariance'],np.zeros((1,9,9)));assert_array_equal(r['final_rotation'],np.eye(3))
def oracle(m):
    rng=np.random.default_rng(853);n=48;phi=rng.normal(size=(n,6))[:,::2]*.2;phi[0]=[1e-9,-2e-9,3e-9];phi[1]=[2.9,0,0];f=rng.normal(size=(n,3));h=rng.uniform(.01,.1,n);q=rng.uniform(.01,.5,(n,6));old=phi.copy();out=m.preintegration_covariance(phi,f,h,q);r=np.eye(3);impulse=np.zeros((9,6*n))
    def cross(x):
        a,b,c=x;return np.array([[0.,-c,b],[c,0.,-a],[-b,a,0.]])
    for k in range(n):
        z=cross(phi[k]);term=np.eye(3);e=np.eye(3);jr=np.eye(3)
        for j in range(1,45):
            term=term@z/j;e+=term;jr+=((-1)**j)*term/(j+1)
        oldnoise=impulse.copy();impulse[:3]=e.T@oldnoise[:3];impulse[3:6]=oldnoise[3:6]-r@cross(f[k])@oldnoise[:3]*h[k];impulse[6:]=oldnoise[6:]+oldnoise[3:6]*h[k]-.5*r@cross(f[k])@oldnoise[:3]*h[k]**2
        impulse[:3,6*k:6*k+3]+=jr*h[k]*np.sqrt(q[k,:3]);impulse[3:6,6*k+3:6*k+6]+=r*h[k]*np.sqrt(q[k,3:]);impulse[6:,6*k+3:6*k+6]+=.5*r*h[k]**2*np.sqrt(q[k,3:]);assert_allclose(out['covariance'][k+1],impulse@impulse.T,atol=1e-10,rtol=1e-8);r=r@e
    assert_allclose(out['final_rotation'],r,atol=1e-10);assert_array_equal(phi,old);assert not np.shares_memory(out['covariance'],q)
def long(m):
    n=1024;phi=np.zeros((n,3));phi[:,2]=.001;f=np.tile([2.,-1.,3.],(n,1));q=np.ones((n,6))*.01;r=m.preintegration_covariance(phi,f,np.full(n,.01),q);p=r['covariance'][-1];assert p.shape==(9,9);assert np.max(abs(p[:3,3:6]))>1e-6;assert np.linalg.eigvalsh(p).min()>-1e-10;assert_allclose(p,p.T,atol=1e-12)
def invalid(m):
    a=[np.zeros((1,3)),np.zeros((1,3)),np.ones(1),np.ones((1,6))]
    for i,v in [(0,np.array([[3.1,0,0]])),(1,np.array([[101.,0,0]])),(2,np.zeros(1)),(3,-np.ones((1,6))),(3,np.full((1,6),np.nan))]:
        b=a.copy();b[i]=v;bad(lambda:m.preintegration_covariance(*b))
TESTS=[('One-step coupled velocity-position uncertainty','public',one),('Empty inertial window','public',empty),('Independent noise impulse Gram oracle with small and large rotations','hidden',oracle),('Full-length nonzero gyro-force coupling and PSD','hidden',long),('Invalid integrated angles durations and variances','hidden',invalid)]
