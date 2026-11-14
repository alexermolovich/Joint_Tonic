import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def tied(m):
 r=m.dustbin_assignment(np.zeros((1,1)),0,1);assert_allclose(r['assignment'],.5);assert not r['row_unmatched'][0] and not r['column_unmatched'][0]
def missing(m):
 r=m.dustbin_assignment(np.array([[-2.]]),0,100);p=1/(1+np.e);assert_allclose(r['assignment'],[[p,1-p],[1-p,p]]);assert r['row_unmatched'][0] and r['column_unmatched'][0]
def oracle(m):
 rng=np.random.default_rng(836);s=rng.normal(size=(64,192))[:,::2];before=s.copy();r=m.dustbin_assignment(s,.3,31);z=np.full((65,97),np.exp(.3));z[:64,:96]=np.exp(s);a=np.r_[np.ones(64),96.]/160;b=np.r_[np.ones(96),64.]/160
 for _ in range(31):z*=a[:,None]/z.sum(axis=1)[:,None];z*=b[None,:]/z.sum(axis=0)[None,:]
 z*=160;assert_allclose(r['assignment'],z,atol=1e-12);assert_array_equal(r['row_unmatched'],z[:64,96]>z[:64,:96].max(axis=1));assert_array_equal(r['column_unmatched'],z[64,:96]>z[:64,:96].max(axis=0));assert_array_equal(s,before);assert not np.shares_memory(r['assignment'],s)
def rectangular(m):
 r=m.dustbin_assignment(np.zeros((2,3)),0,1);expected=np.outer([1,1,3],[1,1,1,2])/5;assert_allclose(r['assignment'],expected);assert r['row_unmatched'].all() and r['column_unmatched'].all()
 r=m.dustbin_assignment(np.array([[100.,-100.],[-100.,100.]]),-100,200);assert np.isfinite(r['assignment']).all();assert not r['row_unmatched'].any()
def invalid(m):
 for s,b,n in [(np.zeros((0,1)),0,1),(np.zeros((1,1)),10**1000,1),(np.zeros((1,1)),0,True),(np.zeros((1,1)),0,201),(np.zeros((1,1),np.float32),0,1)]:bad(lambda:m.dustbin_assignment(s,b,n))
TESTS=[('Dustbin tie policy','public',tied),('Unmatched single pair','public',missing),('Independent rectangular multiplicative transport at scale','hidden',oracle),('Bin capacity and sharp assignments','hidden',rectangular),('Invalid score and iteration bounds','hidden',invalid)]
