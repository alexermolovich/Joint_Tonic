"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def correct(m):
 r=m.check_calibration_gradient(np.array([[2.]]),np.array([1.]),np.array([1.]),np.array([2.]),.001,1e-8);np.testing.assert_allclose(r['numeric'],[2],atol=1e-10);assert r['passed'] and r['relative_error'][0]<1e-8
def wrong(m):
 r=m.check_calibration_gradient(np.array([[2.]]),np.array([1.]),np.array([1.]),np.array([-2.]),.001,1e-8);np.testing.assert_allclose(r['relative_error'],[2]);assert not r['passed']
def zero(m):
 r=m.check_calibration_gradient(np.zeros((2,3)),np.ones(3),np.ones(2),np.zeros(3),1e-6,0);np.testing.assert_array_equal(r['numeric'],[0,0,0]);assert r['passed']
def scale(m):
 rng=np.random.default_rng(12);a=rng.normal(size=(64,64))[:,::2];x=rng.normal(size=32);b=rng.normal(size=64);g=a.T@(a@x-b);before=x.copy()
 # Scale design to keep supplied analytic gradient within the public bound.
 a=a/10;g=a.T@(a@x-b);r=m.check_calibration_gradient(a,x,b,g,.001,1e-7);np.testing.assert_allclose(r['numeric'],g,atol=1e-9);assert r['passed'];np.testing.assert_array_equal(x,before);assert not np.shares_memory(r['numeric'],x)
 bad=g.copy();bad[3]+=1;r=m.check_calibration_gradient(a,x,b,bad,.001,1e-7);assert not r['passed'] and r['relative_error'][3]>1e-4
 # Verify actual finite differences, not the supplied analytic gradient.
 r=m.check_calibration_gradient(a,x,b,np.zeros(32),.001,1);np.testing.assert_allclose(r['numeric'],g,atol=1e-9)
def invalid(m):
 good=[np.ones((1,1)),np.ones(1),np.ones(1),np.ones(1),.001,.01]
 for i,value in [(0,np.ones((1,1),dtype=np.float32)),(0,np.full((1,1),np.nan)),(1,np.ones(2)),(3,np.array([101.])),(4,0),(4,True),(5,-1),(5,10**1000)]:
  a=[v.copy() if isinstance(v,np.ndarray) else v for v in good];a[i]=value;rejects(lambda:m.check_calibration_gradient(*a))

TESTS=[('Correct calibration derivative', 'public', correct), ('Wrong sign rejected', 'public', wrong), ('Zero sensitivity and exact tolerance', 'hidden', zero), ('Independent analytic oracle on strided design', 'hidden', scale), ('Invalid derivative contract', 'hidden', invalid)]
