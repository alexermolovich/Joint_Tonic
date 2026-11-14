import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.balanced_latent_loss([[[0,0]]],[[[0,0]]],[2],[True]);assert_allclose(r['kl'],[0]);assert r['loss']==3.1;assert not r['prior_gradient'].any() and not r['posterior_gradient'].any();assert_array_equal(r['prediction_gradient'],[1])

def missing(m):
    r=m.balanced_latent_loss([[[0,0]]],[[[0,0]]],[2],[False]);assert r['loss']==0 and np.isnan(r['kl']).all() and not r['prediction_gradient'].any()
    r=m.balanced_latent_loss([[[0,0]],[[0,0]]],[[[0,0]],[[0,0]]],[2,4],[True,True]);assert_allclose(r['loss'],4.1);assert_array_equal(r['prediction_gradient'],[.5,.5])

def derivatives(m):
    ql=np.array([[[4.,-4.,0.],[3.,-3.,0.]]]);pl=-ql;pred=np.array([.3]);v=np.array([True]);r=m.balanced_latent_loss(ql,pl,pred,v);assert r['kl'][0]>1
    def prob(x):
        e=np.exp(x-x.max(axis=-1,keepdims=True));return .99*e/e.sum(axis=-1,keepdims=True)+.01/x.shape[-1]
    q=prob(ql);p=prob(pl);eps=1e-5
    # Each objective freezes the opposite distribution, matching stop-gradient semantics.
    for idx in np.ndindex(ql.shape):
        hi=pl.copy();lo=pl.copy();hi[idx]+=eps;lo[idx]-=eps
        gp=(np.sum(q*np.log(q/prob(hi)))-np.sum(q*np.log(q/prob(lo))))/(2*eps)
        hi=ql.copy();lo=ql.copy();hi[idx]+=eps;lo[idx]-=eps;qh=prob(hi);qlow=prob(lo)
        gq=.1*(np.sum(qh*np.log(qh/p))-np.sum(qlow*np.log(qlow/p)))/(2*eps)
        assert_allclose(r['prior_gradient'][idx],gp,atol=1e-9);assert_allclose(r['posterior_gradient'][idx],gq,atol=1e-9)
    ql=np.zeros((128,32,64))[:,:,::2];ql[:,:,0]=10;pl=-ql;before=ql.copy();r=m.balanced_latent_loss(ql,pl,np.zeros(128),np.ones(128,bool));assert np.isfinite(r['prior_gradient']).all();assert_allclose(r['prior_gradient'].sum(axis=-1),0,atol=1e-14);assert_array_equal(ql,before);assert not np.shares_memory(r['posterior_gradient'],ql)
    # One masked active row must not change valid normalization.
    a=m.balanced_latent_loss([[[4,-4]]],[[[-4,4]]],[0],[True]);b=m.balanced_latent_loss([[[4,-4]],[[4,-4]]],[[[-4,4]],[[-4,4]]],[0,0],[True,False]);assert_allclose(a['prior_gradient'][0],b['prior_gradient'][0]);assert not b['posterior_gradient'][1].any()

def invalid(m):
    for a in [([[[51,0]]],[[[0,0]]],[0],[True]),([[[0,0]]],[[[0,0]]],[-1],[True]),([[[0,0]]],[[[0,0]]],[0],[1]),([[[np.nan,0]]],[[[0,0]]],[0],[False])]:bad(lambda:m.balanced_latent_loss(*a))
TESTS=[('Free-nat loss with no KL gradient','public',one),('Missing rows and prediction normalization','public',missing),('Independent frozen-path finite differences and scale','hidden',derivatives),('Invalid latent model loss','hidden',invalid)]
