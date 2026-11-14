import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def uniform(m):assert_allclose(m.latent_sequence([[.5,.5]],[[[0]]],np.zeros((2,2)),[[0,0]],[0,0],2),[[[.5,.5],[.5,.5]]])
def action(m):assert_allclose(m.latent_sequence([[.5,.5]],[[[1]]],np.zeros((2,2)),[[0,np.log(3)]],[0,0],2)[0,1],[.25,.75])
def oracle(m):
    rng=np.random.default_rng(544);z=np.array([[.25,.75,.5,.5]]);a=rng.normal(size=(1,4,2));w=rng.normal(size=(4,4));u=rng.normal(size=(2,4));bias=rng.normal(size=4);r=m.latent_sequence(z,a,w,u,bias,2);current=z[0]
    for t in range(4):
        raw=np.array([sum(current[j]*w[j,k] for j in range(4))+sum(a[0,t,j]*u[j,k] for j in range(2))+bias[k] for k in range(4)]);current=np.concatenate([np.exp(raw[g:g+2])/np.exp(raw[g:g+2]).sum() for g in [0,2]]);assert_allclose(r[0,t+1],current)
    z=np.full((32,64),.25)[:,::2];before=z.copy();r=m.latent_sequence(z,np.ones((32,64,32)),np.ones((32,32)),np.ones((32,32)),np.zeros(32),4);assert r.shape==(32,65,32);assert_allclose(r.reshape(32,65,8,4).sum(axis=-1),1);assert_array_equal(z,before);assert not np.shares_memory(r,z)
    r=m.latent_sequence([[1]],np.empty((1,0,1)),[[1]],[[1]],[0],1);assert_array_equal(r,[[[1]]])
def invalid(m):
    for z,a in [([[.1,.1]],[[[0]]]),([[-.5,1.5]],[[[0]]]),([[.5,.5]],[[[11]]])]:bad(lambda:m.latent_sequence(z,a,np.zeros((2,2)),[[0,0]],[0,0],2))
TESTS=[('Uniform next simplex','public',uniform),('Action-conditioned ratios','public',action),('Independent recurrence oracle and group invariants at scale','hidden',oracle),('Invalid initial simplex or dynamics','hidden',invalid)]
