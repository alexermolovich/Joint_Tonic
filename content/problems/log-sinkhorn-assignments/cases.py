import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def uniform(m):
 r=m.sinkhorn_assignments(np.zeros((2,2)),np.full(2,.5),np.full(2,.5),1);assert_allclose(r['transport'],.25);assert_allclose(r['log_transport'],np.log(.25));assert r['row_error']<1e-14
def nonuniform(m):
 r=m.sinkhorn_assignments(np.zeros((2,2)),np.array([.75,.25]),np.full(2,.5),1);assert_allclose(r['transport'],[[.375,.375],[.125,.125]])
def oracle(m):
 rng=np.random.default_rng(835);s=rng.normal(size=(64,192))[:,::2];a=rng.uniform(.1,1,64);a/=a.sum();b=rng.uniform(.1,1,96);b/=b.sum();before=s.copy();r=m.sinkhorn_assignments(s,a,b,17)
 # Independent multiplicative Sinkhorn on a positive moderate-score kernel.
 p=np.exp(s)
 for _ in range(17):
  p*=a[:,None]/p.sum(axis=1)[:,None];p*=b[None,:]/p.sum(axis=0)[None,:]
 assert_allclose(r['transport'],p,atol=1e-12);assert_allclose(r['log_transport'],np.log(p));assert_allclose(r['row_error'],max(abs(p.sum(axis=1)-a)),atol=1e-14);assert_allclose(r['column_error'],max(abs(p.sum(axis=0)-b)),atol=1e-14);assert_array_equal(s,before);assert not np.shares_memory(r['transport'],s)
def peaked(m):
 s=np.array([[100.,-100.],[-100.,100.]]);a=np.array([.9,.1]);b=np.array([.1,.9]);r=m.sinkhorn_assignments(s,a,b,1);assert r['row_error']>.7;assert r['column_error']<1e-12;assert np.isfinite(r['log_transport']).all()
 later=m.sinkhorn_assignments(s,a,b,200);assert later['row_error']<1e-8
 r=m.sinkhorn_assignments(np.array([[100.]]),np.ones(1),np.ones(1),1);assert_allclose(r['transport'],[[1]])
 near=np.array([.5,.5+5e-10]);r=m.sinkhorn_assignments(np.zeros((2,1)),near,np.ones(1),1);assert_allclose(r['transport'][:,0],near/near.sum())
def invalid(m):
 for s,a,b,n in [(np.zeros((2,2)),np.array([0.,1.]),np.full(2,.5),1),(np.zeros((2,2)),np.array([.2,.2]),np.full(2,.5),1),(np.zeros((1,1)),np.ones(1),np.ones(1),True),(np.zeros((1,1)),np.ones(1),np.ones(1),10**1000),(np.ones((1,1))*101,np.ones(1),np.ones(1),1)]:bad(lambda:m.sinkhorn_assignments(s,a,b,n))
TESTS=[('Uniform transport','public',uniform),('Nonuniform row budgets','public',nonuniform),('Independent multiplicative normalization at scale','hidden',oracle),('Peaked logits finite iterations singleton and normalized tolerance','hidden',peaked),('Invalid marginals iterations and scores','hidden',invalid)]
