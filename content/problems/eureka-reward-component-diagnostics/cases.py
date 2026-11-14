import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.reward_diagnostics([[[1,2],[3,2]]],[[0,1]],[[True,True]]);assert_array_equal(r['mean'],[2,2]);assert_array_equal(r['std'],[1,0]);assert_allclose(r['correlation'],[1,np.nan]);assert r['count']==2

def single(m):
    r=m.reward_diagnostics([[[1,2],[3,2]]],[[0,1]],[[False,True]]);assert_array_equal(r['mean'],[3,2]);assert_array_equal(r['std'],[0,0]);assert np.isnan(r['correlation']).all()

def oracle(m):
    rng=np.random.default_rng(535);x=rng.normal(size=(32,512,32))[:,:,::2];y=rng.normal(size=(32,512));v=rng.random((32,512))>.2;before=x.copy();r=m.reward_diagnostics(x,y,v);a=x[v];assert_allclose(r['mean'],np.mean(a,axis=0));assert_allclose(r['std'],np.std(a,axis=0));assert_allclose(r['mean_abs'],np.abs(a).mean(axis=0));assert_allclose(r['correlation'],[np.corrcoef(a[:,j],y[v])[0,1] for j in range(16)],atol=1e-12);assert_array_equal(x,before);assert not np.shares_memory(r['mean'],x)
    r=m.reward_diagnostics([[[1e-200],[2e-200]]],[[0,1]],[[True,True]]);assert_allclose(r['correlation'],[1]);assert_allclose(r['std']/1e-200,[.5])
    r=m.reward_diagnostics([[[1]]],[[2]],[[False]]);assert r['count']==0 and np.isnan(r['mean']).all()

def invalid(m):
    bad(lambda:m.reward_diagnostics([[[np.nan]]],[[0]],[[False]]));bad(lambda:m.reward_diagnostics([[[0]]],[[0]],[[1]]))
TESTS=[('Varying and constant terms','public',one),('One observation','public',single),('Independent population oracle tiny values and scale','hidden',oracle),('Invalid diagnostics','hidden',invalid)]
