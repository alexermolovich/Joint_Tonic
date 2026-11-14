"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def mass(m):
 r=m.constrain_randomization_bounds(np.array([2.]),np.array([[.5,3.]]),np.array([[1.,4.]]),np.array([.2]));np.testing.assert_allclose(r['bounds'],[[1.2,3]]);np.testing.assert_array_equal(r['feasible'],[True]);assert r['failed_dimensions'].shape==(0,)
def consumed(m):
 r=m.constrain_randomization_bounds(np.array([.05]),np.array([[0.,.1]]),np.array([[0.,.1]]),np.array([.06]));assert not r['feasible'][0] and np.isnan(r['bounds']).all();np.testing.assert_array_equal(r['failed_dimensions'],[0])
def nominal(m):
 r=m.constrain_randomization_bounds(np.array([0.,1.,2.]),np.array([[0.,0.],[0.,2.],[0.,1.]]),np.array([[0.,2.]]*3),np.zeros(3));np.testing.assert_array_equal(r['feasible'],[True,True,False]);np.testing.assert_array_equal(r['bounds'][:2],[[0,0],[0,2]]);assert np.isnan(r['bounds'][2]).all()
def scale(m):
 rng=np.random.default_rng(10);req=np.sort(rng.uniform(-3,3,(64,2)),axis=1);allowed=np.tile([-2.,2.],(64,1));margins=np.arange(128,dtype=float)[::2]/100;nom=np.linspace(-2,2,64);before=req.copy();r=m.constrain_randomization_bounds(nom,req,allowed,margins)
 for j in range(64):
  lo=max(req[j,0],-2+margins[j]);hi=min(req[j,1],2-margins[j]);ok=lo<=nom[j]<=hi;assert r['feasible'][j]==ok
  if ok:np.testing.assert_array_equal(r['bounds'][j],[lo,hi])
  else:assert np.isnan(r['bounds'][j]).all()
 np.testing.assert_array_equal(req,before);np.testing.assert_array_equal(r['failed_dimensions'],[i for i,x in enumerate(r['feasible']) if not x]);assert not np.shares_memory(r['bounds'],req)
def invalid(m):
 good=[np.zeros(1),np.array([[0.,1.]]),np.array([[0.,1.]]),np.zeros(1)]
 for i,value in [(0,np.zeros(1,dtype=np.float32)),(1,np.array([[1.,0.]])),(2,np.array([[np.nan,1.]])),(3,np.array([-1.])),(1,np.zeros((1,3))),(0,np.zeros(0))]:
  a=[x.copy() for x in good];a[i]=value;rejects(lambda:m.constrain_randomization_bounds(*a))

TESTS=[('Feasible mass interval', 'public', mass), ('Margin consumes interval', 'public', consumed), ('Nominal inclusion and singleton boundaries', 'hidden', nominal), ('Scalar physical interval oracle', 'hidden', scale), ('Invalid input intervals', 'hidden', invalid)]
