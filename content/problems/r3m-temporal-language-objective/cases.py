import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.representation_objective(np.zeros((1,4,1)),[[0,0,0]],[True],[1,1,1,1]);assert_allclose(r['components'],[np.log(3),np.log(3),0,0]);assert_allclose(r['loss'],2*np.log(3))

def regularization(m):
    r=m.representation_objective(np.tile([3.,4.],(1,4,1)),[[0,0,0]],[True],[0,0,2,3]);assert_allclose(r['components'],[np.log(3),np.log(3),7,5]);assert r['loss']==29

def oracle(m):
    rng=np.random.default_rng(556);z=rng.normal(size=(128,4,64))[:,:,::2];g=rng.normal(size=(128,3));mask=rng.random(128)>.3;w=np.array([.2,.4,.01,.02]);before=z.copy();out=m.representation_objective(z,g,mask,w);expected=np.zeros((128,4))
    for i in range(128):
        if not mask[i]:continue
        logits=[-sum(float(a-b)**2 for a,b in zip(z[i,0],z[i,j]))**.5 for j in range(1,4)];p=np.exp(np.array(logits)-max(logits));p/=sum(p);q=np.exp(g[i]-max(g[i]));q/=sum(q);expected[i]=[-np.log(p[0]),-np.log(q[0]),sum(abs(z[i,0])),sum(z[i,0]**2)**.5]
    assert_allclose(out['per_example'],expected,atol=1e-12);assert_allclose(out['components'],expected.sum(axis=0)/mask.sum());assert_allclose(out['loss'],sum(out['components']*w));assert_array_equal(z,before);assert not np.shares_memory(out['per_example'],z)
    r=m.representation_objective(np.zeros((512,4,256)),np.tile([-1000.,1000.,0.],(512,1)),np.ones(512,bool),[0,1,0,0]);assert_allclose(r['loss'],2000)
    for b in [0,2]:
        r=m.representation_objective(np.zeros((b,4,1)),np.zeros((b,3)),np.zeros(b,bool),[1]*4);assert r['loss']==0;assert_array_equal(r['components'],np.zeros(4))

def invalid(m):
    for z,g,v,w in [(np.full((1,4,1),101),[[0,0,0]],[False],[1]*4),(np.zeros((1,4,1)),[[np.nan,0,0]],[False],[1]*4),(np.zeros((1,4,1)),[[0,0,0]],[True],[-1,0,0,0]),(np.zeros((1,3,1)),[[0,0,0]],[True],[1]*4)]:bad(lambda:m.representation_objective(z,g,v,w))
TESTS=[('Equal contrastive scores','public',one),('L1 and nonsquared L2 terms','public',regularization),('Independent distance softmax oracle masked reduction extreme logits and scale','hidden',oracle),('Invalid masked objective inputs','hidden',invalid)]
