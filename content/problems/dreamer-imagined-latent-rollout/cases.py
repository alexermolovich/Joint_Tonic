import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.imagine_latents([[0]],[[[0]]],[[0]],[[0]],[0],[0],0,[0],0);assert_array_equal(r['states'],[[[0],[0]]]);assert_array_equal(r['rewards'],[[0]]);assert_array_equal(r['continuation'],[[.5]])

def action(m):
    r=m.imagine_latents([[0]],[[[1]]],[[0]],[[1]],[0],[2],1,[0],0);assert_allclose(r['states'][0,1],np.tanh(1));assert_allclose(r['rewards'],[[2*np.tanh(1)+1]])

def oracle(m):
    rng=np.random.default_rng(542);x=rng.normal(size=(2,3));a=rng.normal(size=(2,4,2));w=rng.normal(size=(3,3));u=rng.normal(size=(2,3));b=rng.normal(size=3);rw=rng.normal(size=3);cw=rng.normal(size=3);r=m.imagine_latents(x,a,w,u,b,rw,.3,cw,-.2)
    for row in range(2):
        state=x[row].copy()
        for t in range(4):
            state=np.array([np.tanh(sum(state[j]*w[j,k] for j in range(3))+sum(a[row,t,j]*u[j,k] for j in range(2))+b[k]) for k in range(3)]);assert_allclose(r['states'][row,t+1],state);assert_allclose(r['rewards'][row,t],sum(state*rw)+.3);assert_allclose(r['continuation'][row,t],1/(1+np.exp(-(sum(state*cw)-.2))))
    x=np.ones((32,64))[:,::2];before=x.copy();r=m.imagine_latents(x,np.ones((32,64,32)),np.ones((32,32)),np.ones((32,32)),np.ones(32),np.ones(32),0,-np.ones(32)*10,-10);assert r['states'].shape==(32,65,32);assert np.isfinite(r['continuation']).all();assert np.all(r['continuation']<1e-100);assert np.all(r['states'][:,1:]>.9);assert_array_equal(x,before);assert not np.shares_memory(r['states'],x)
    r=m.imagine_latents([[1]],np.empty((1,0,1)),[[1]],[[1]],[0],[1],0,[1],0);assert_array_equal(r['states'],[[[1]]]);assert r['rewards'].shape==(1,0)

def invalid(m):
    bad(lambda:m.imagine_latents([[11]],[[[0]]],[[0]],[[0]],[0],[0],0,[0],0));bad(lambda:m.imagine_latents([[0]],[[[0]]],[[0]],[[0]],[0],[0],10**1000,[0],0));bad(lambda:m.imagine_latents([[0]],[[[0]]],[[0]],[[0]],[0],[0],0,[np.nan],0))
TESTS=[('Zero dynamics','public',one),('Action-conditioned successor heads','public',action),('Scalar rollout oracle tiny continuation empty horizon and scale','hidden',oracle),('Invalid latent dynamics','hidden',invalid)]
