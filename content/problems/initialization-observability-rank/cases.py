import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def full(m):
 r=m.initialization_rank(np.diag([2.,1.]),np.ones(2),np.ones(2),.001);assert_array_equal(r['singular_values'],[2,1]);assert r['rank']==2 and r['observable'] and r['condition']==2;assert_allclose(r['unobservable_projector'],np.zeros((2,2)))
def deficient(m):
 r=m.initialization_rank(np.array([[1.,0.]]),np.ones(2),np.ones(1),.001);assert_array_equal(r['singular_values'],[1,0]);assert r['rank']==1 and not r['observable'] and np.isinf(r['condition']);assert_array_equal(r['unobservable_projector'],np.diag([0,1]))
def oracle(m):
 rng=np.random.default_rng(842);left,_=np.linalg.qr(rng.normal(size=(1024,16)));right,_=np.linalg.qr(rng.normal(size=(16,16)));s=np.r_[np.linspace(5,1,12),np.zeros(4)];a=(left*s)@right.T;scales=np.linspace(.5,2,16);std=np.linspace(.5,2,1024);raw=a*std[:,None]/scales;storage=np.zeros((1024,32));storage[:,::2]=raw;j=storage[:,::2];before=j.copy();r=m.initialization_rank(j,scales,std,1e-6);p=r['unobservable_projector'];expected=right[:,12:]@right[:,12:].T
 assert r['rank']==12;assert_allclose(r['singular_values'],s,atol=1e-12);assert_allclose(p,expected,atol=1e-12);assert_allclose(p@p,p,atol=1e-12);assert_allclose(p.T,p,atol=1e-12);assert_allclose(a@p,0,atol=1e-12);assert_allclose(np.trace(p),4);assert_array_equal(j,before);assert not np.shares_memory(p,j)
def edges(m):
 r=m.initialization_rank(np.empty((0,3)),np.ones(3),np.empty(0),.001);assert r['rank']==0;assert_array_equal(r['unobservable_projector'],np.eye(3))
 r=m.initialization_rank(np.diag([1.,.01]),np.ones(2),np.ones(2),.01);assert r['rank']==1
 r=m.initialization_rank(np.zeros((4,3)),np.ones(3),np.ones(4),.001);assert r['rank']==0
def invalid(m):
 for j,s,std,c in [(np.ones((1,1),np.float32),np.ones(1),np.ones(1),.001),(np.ones((1,1)),np.zeros(1),np.ones(1),.001),(np.ones((1,1)),np.ones(1),np.ones(1),10**1000)]:bad(lambda:m.initialization_rank(j,s,std,c))
TESTS=[('Fully constrained scaled system','public',full),('One missing parameter direction','public',deficient),('Constructed singular spectrum and projector invariants at scale','hidden',oracle),('Empty zero and cutoff equality','hidden',edges),('Invalid scaling and sensitivity contract','hidden',invalid)]
