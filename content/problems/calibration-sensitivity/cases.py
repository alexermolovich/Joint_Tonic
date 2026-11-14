"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def angular(m):
 r=m.calibration_sensitivity(np.array([.5]),np.array([[.8]]),np.array([[.4]]),np.array([.1]),np.array([.02]));np.testing.assert_allclose(r['slope'],[[2]]);np.testing.assert_allclose(r['curvature'],[[20]]);np.testing.assert_allclose(r['scaled_sensitivity'],[[.04]]);np.testing.assert_array_equal(r['ranking'],[0])
def tie(m):
 r=m.calibration_sensitivity(np.array([0.]),np.array([[2.],[4.]]),np.array([[-2.],[-4.]]),np.array([1.,2.]),np.array([1.,1.]));np.testing.assert_array_equal(r['ranking'],[0,1]);np.testing.assert_array_equal(r['slope'],[[2],[2]]);assert not r['curvature'].any()
def polynomial(m):
 k=64;n=64;linear=np.arange(k*n,dtype=float).reshape(k,n)/4096;quadratic=linear[::-1];d=np.linspace(.1,1,k);s=np.linspace(1,.1,k);base=np.ones(n);plus=base+linear*d[:,None]+quadratic*d[:,None]**2;minus=base-linear*d[:,None]+quadratic*d[:,None]**2
 a=np.empty((k,n*2));a[:,::2]=plus;pc=plus.copy();r=m.calibration_sensitivity(base,a[:,::2],minus,d,s);np.testing.assert_allclose(r['slope'],linear,atol=1e-12);np.testing.assert_allclose(r['curvature'],2*quadratic,atol=1e-12);np.testing.assert_allclose(r['scaled_sensitivity'],linear*s[:,None]);np.testing.assert_array_equal(plus,pc)
 expected=sorted(range(k),key=lambda i:(-max(linear[i]*s[i]),i));np.testing.assert_array_equal(r['ranking'],expected)
def signed(m):
 r=m.calibration_sensitivity(np.array([0.,0.]),np.array([[-2.,1.],[1.,1.]]),np.array([[2.,-1.],[-1.,-1.]]),np.ones(2),np.ones(2));np.testing.assert_array_equal(r['slope'],[[-2,1],[1,1]]);np.testing.assert_array_equal(r['scaled_sensitivity'],[[2,1],[1,1]]);np.testing.assert_array_equal(r['ranking'],[0,1]);assert not np.shares_memory(r['slope'],r['scaled_sensitivity'])
def invalid(m):
 good=[np.zeros(1),np.zeros((1,1)),np.zeros((1,1)),np.ones(1),np.ones(1)]
 for i,value in [(0,np.array([0],dtype=np.float32)),(1,np.zeros((1,2))),(2,np.full((1,1),np.nan)),(3,np.array([0.])),(4,np.array([-1.])),(0,np.zeros(0)),(1,np.zeros((65,1)))]:
  args=[x.copy() for x in good];args[i]=value;rejects(lambda:m.calibration_sensitivity(*args))

TESTS=[('Angular calibration perturbation', 'public', angular), ('Deterministic ranking tie', 'public', tie), ('Independent quadratic model derivative oracle', 'hidden', polynomial), ('Signed slopes versus absolute sensitivity', 'hidden', signed), ('Invalid perturbation contract', 'hidden', invalid)]
