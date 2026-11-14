import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def ties(m):
 r=m.coarse_matches(np.zeros((2,1)),np.zeros((2,1)),np.ones(2,bool),np.ones(2,bool),1,0);assert_allclose(r['confidence'],.25);assert_array_equal(r['pairs'],[[0,0]]);assert_allclose(r['match_confidence'],[.25])
def masked(m):
 r=m.coarse_matches(np.zeros((2,1)),np.zeros((2,1)),np.ones(2,bool),np.array([True,False]),1,0);assert_allclose(r['confidence'],[[.5,0],[.5,0]]);assert_array_equal(r['pairs'],[[0,0]])
def oracle(m):
 rng=np.random.default_rng(839);a=rng.normal(size=(128,32))[:,::2];b=rng.normal(size=(192,32))[:,::2];ma=rng.random(128)>.2;mb=rng.random(192)>.2;before=a.copy();r=m.coarse_matches(a,b,ma,mb,.2,0);p=np.zeros((128,192));ia=np.flatnonzero(ma);ib=np.flatnonzero(mb);s=np.array([[sum(a[i]*b[j])/3.2 for j in ib] for i in ia]);e=np.exp(s);real=e/e.sum(axis=1)[:,None]*e/e.sum(axis=0)[None,:];p[np.ix_(ia,ib)]=real;expected=[]
 for i in ia:
  j=max(ib,key=lambda j:p[i,j]);ii=max(ia,key=lambda ii:p[ii,j])
  if ii==i:expected.append([i,j])
 assert_allclose(r['confidence'],p,atol=1e-12);assert_array_equal(r['pairs'],np.array(expected).reshape(-1,2));assert_allclose(r['match_confidence'],[p[i,j] for i,j in expected]);assert_array_equal(a,before);assert not np.shares_memory(r['confidence'],a)
def edges(m):
 r=m.coarse_matches(np.zeros((2,1)),np.zeros((2,1)),np.ones(2,bool),np.ones(2,bool),1,.25);assert r['pairs'].shape==(0,2)
 for n,ma in [(0,np.empty(0,bool)),(2,np.zeros(2,bool))]:
  r=m.coarse_matches(np.ones((n,2)),np.ones((3,2)),ma,np.ones(3,bool),1,0);assert r['confidence'].shape==(n,3);assert not r['confidence'].any();assert r['pairs'].shape==(0,2)
 a=np.array([[100.,100.],[-100.,-100.]]);r=m.coarse_matches(a,a,np.ones(2,bool),np.ones(2,bool),.001,.5);assert_array_equal(r['pairs'],[[0,0],[1,1]]);assert np.isfinite(r['confidence']).all()
def invalid(m):
 for tau,th in [(0,0),(10**1000,0),(1,True),(1,-1)]:bad(lambda:m.coarse_matches(np.ones((1,1)),np.ones((1,1)),np.ones(1,bool),np.ones(1,bool),tau,th))
 bad(lambda:m.coarse_matches(np.ones((1,2)),np.ones((1,3)),np.ones(1,bool),np.ones(1,bool),1,0))
TESTS=[('Dual normalization tie','public',ties),('Exclude padded target before normalization','public',masked),('Independent probability and mutual oracle at scale','hidden',oracle),('Strict threshold empty support and extreme logits','hidden',edges),('Invalid feature and scalar contract','hidden',invalid)]
