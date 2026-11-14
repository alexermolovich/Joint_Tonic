import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.sample_ddpm_actions([[1]],[[[0]]],[.04],[[[99]]]);assert_allclose(r[:,0,0],[1,1/np.sqrt(.96)])
def example2(m):
    r=m.sample_ddpm_actions([[0]],np.zeros((2,1,1)),[.04,.04],[[[0]],[[1]]]);v=np.sqrt(.04*.04/.0784);assert_allclose(r[:,0,0],[0,v,v/np.sqrt(.96)])
def mechanisms(m):
    x=np.array([[1.,2.],[-1.,0.]]);before=x.copy();r=m.sample_ddpm_actions(x,np.zeros((3,2,2)),[.01,.04,.09],np.zeros((3,2,2)))
    assert_allclose(r[-1],x/np.sqrt(.99*.96*.91));assert_array_equal(x,before);assert not np.shares_memory(r,x)
    r=m.sample_ddpm_actions([[0]],[[[2]]],[.04],[[[0]]]);assert_allclose(r[-1,0,0],-.4/np.sqrt(.96))
def invalid(m):
    good=[[[1]],[[[0]]],[.04],[[[0]]]]
    for i,v in [(0,[]),(1,np.zeros((2,1,1))),(2,[0]),(2,[.2]),(3,[[[np.nan]]]),(0,[[101]]),(0,[[True]])]:
        a=good.copy();a[i]=v;bad(lambda:m.sample_ddpm_actions(*a))
TESTS=[('Final reverse step omits noise','public',example1),('Posterior variance','public',example2),('Schedule and noise prediction mechanisms','hidden',mechanisms),('Invalid sampler contract','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    x=np.ones((32,64))[:,::2];e=np.zeros((16,32,32));z=e.copy();b=np.full(16,.01);copy=x.copy();r=m.sample_ddpm_actions(x,e,b,z)
    assert r.shape==(17,32,32) and r.dtype==np.float64;assert_allclose(r[-1],x/(.99**8));assert_array_equal(x,copy);assert not np.shares_memory(r,x)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
