import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.latent_supervision([[0]],[[1]],[0],[[2]],[True]);assert_array_equal(r['targets'],[[0]]);assert r['loss']==4;assert_array_equal(r['prediction_gradient'],[[4]])
def channels(m):
    r=m.latent_supervision([[0]],[[1,1]],[0,0],[[1,-1]],[True]);assert r['loss']==1;assert_array_equal(r['prediction_gradient'],[[1,-1]])
def scale(m):
    rng=np.random.default_rng(529);e=rng.normal(size=(128,64))[:,::2];w=rng.normal(size=(32,32));b=np.zeros(32);p=np.zeros((128,32));v=np.ones(128,bool);v[::2]=False;r=m.latent_supervision(e,w,b,p,v);assert not np.shares_memory(r['targets'],e);assert np.isnan(r['per_state'][::2]).all();h=1e-5;hi=p.copy();lo=p.copy();hi[1,0]+=h;lo[1,0]-=h;assert_allclose((m.latent_supervision(e,w,b,hi,v)['loss']-m.latent_supervision(e,w,b,lo,v)['loss'])/(2*h),r['prediction_gradient'][1,0],atol=1e-8)
    r=m.latent_supervision([[1]],[[2]],[1],[[1]],[False]);assert r['loss']==0 and r['targets'][0,0]==0 and np.isnan(r['per_state'][0])
def invalid(m):
    for a in [([[101]],[[1]],[0],[[1]],[False]),([[0]],[[1]],[0],[[1]],[1]),([[0]],[[1,1]],[0],[[1]],[True])]:bad(lambda:m.latent_supervision(*a))
TESTS=[('Frozen target error','public',one),('Latent dimension mean','public',channels),('Scale masks and finite difference','hidden',scale),('Invalid supervision','hidden',invalid)]
