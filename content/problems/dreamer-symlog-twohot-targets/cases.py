import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    x=[0,np.expm1(1)];r=m.symlog_twohot(x,[-1,0,2]);assert_allclose(r['symlog'],[0,1]);assert_array_equal(r['targets'],[[0,1,0],[0,.5,.5]]);assert_allclose(r['reconstructed'],x)

def clip(m):
    r=m.symlog_twohot([-100,100],[-1,0,1]);assert_array_equal(r['targets'],[[1,0,0],[0,0,1]]);assert_allclose(r['reconstructed'],[-np.expm1(1),np.expm1(1)])

def oracle(m):
    x=np.linspace(-1e4,1e4,8192)[::2];bins=np.linspace(-10,10,127);before=x.copy();r=m.symlog_twohot(x,bins);assert_allclose(r['targets'].sum(axis=1),1);assert (np.count_nonzero(r['targets'],axis=1)<=2).all();assert_allclose(r['targets']@bins,np.sign(x)*np.log1p(np.abs(x)),atol=1e-12);assert_allclose(r['reconstructed'],x,rtol=1e-12);assert_array_equal(x,before);assert not np.shares_memory(r['reconstructed'],x)
    r=m.symlog_twohot([0,np.expm1(1),-np.expm1(1)],[-1,0,1]);assert_array_equal(r['targets'],[[0,1,0],[0,0,1],[1,0,0]])
    assert m.symlog_twohot([],[-1,1])['targets'].shape==(0,2)

def invalid(m):
    for a in [([1],[0,0]),([1],[0]),([1],[-21,0]),([True],[0,1]),([np.nan],[0,1]),(np.zeros(4096),np.linspace(-1,1,255))]:bad(lambda:m.symlog_twohot(*a))
TESTS=[('Two adjacent transformed bins','public',one),('Support clipping','public',clip),('Expectation invariance centers empty and scale','hidden',oracle),('Invalid bins and reward inputs','hidden',invalid)]
