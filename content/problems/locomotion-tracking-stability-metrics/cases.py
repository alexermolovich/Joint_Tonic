import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.gait_metrics([[[.8,.1,.2]]],[[[.1,.2,.3]]],[[[1,0,.5]]],[[[0,0,-1]]],[[True]],.25,.25);expected=[np.exp(-.2),np.exp(-.16),.04,.05,0];assert_allclose(r['per_step'],[[expected]]);assert_allclose(r['means'],[expected]);assert_array_equal(r['counts'],[1])
def tilt(m):
    r=m.gait_metrics(np.zeros((1,1,3)),np.zeros((1,1,3)),np.zeros((1,1,3)),[[[1,0,0]]],[[True]],1,1);assert_array_equal(r['means'],[[1,1,0,0,1]])
def oracle(m):
    rng=np.random.default_rng(558);v=rng.normal(size=(128,256,6))[:,:,::2];w=rng.normal(size=v.shape);c=rng.normal(size=v.shape);g=rng.normal(size=v.shape);g/=np.linalg.norm(g,axis=2,keepdims=True);mask=rng.random((128,256))>.2;mask[0]=False;before=v.copy();out=m.gait_metrics(v,w,c,g,mask,.3,.7);expected=np.zeros((128,256,5))
    for b in range(128):
        for t in range(256):
            if mask[b,t]:expected[b,t]=[np.exp(-sum((v[b,t,:2]-c[b,t,:2])**2)/.3),np.exp(-(w[b,t,2]-c[b,t,2])**2/.7),v[b,t,2]**2,sum(w[b,t,:2]**2),sum(g[b,t,:2]**2)]
    assert_allclose(out['per_step'],expected);assert_allclose(out['means'][1:],np.array([expected[b].sum(axis=0)/mask[b].sum() for b in range(1,128)]));assert np.isnan(out['means'][0]).all();assert_array_equal(v,before);assert not np.shares_memory(out['per_step'],v)
    r=m.gait_metrics(np.empty((0,1,3)),np.empty((0,1,3)),np.empty((0,1,3)),np.empty((0,1,3)),np.empty((0,1),bool),1,1);assert r['means'].shape==(0,5)
    r=m.gait_metrics(np.zeros((1,1,3)),np.zeros((1,1,3)),np.zeros((1,1,3)),[[[0,0,1]]],[[True]],1,1);assert r['means'][0,4]==0
def invalid(m):
    for g,scale in [([[[0,0,0]]],1),([[[0,0,-1]]],0),([[[0,0,-1]]],10**1000),([[[np.nan,0,0]]],1)]:bad(lambda:m.gait_metrics(np.zeros((1,1,3)),np.zeros((1,1,3)),np.zeros((1,1,3)),g,[[False]],scale,1))
TESTS=[('Tracking and stability terms','public',one),('Horizontal gravity penalty','public',tilt),('Scalar trace oracle realistic strided scale empty and missing evidence','hidden',oracle),('Invalid gravity and scales even when masked','hidden',invalid)]
