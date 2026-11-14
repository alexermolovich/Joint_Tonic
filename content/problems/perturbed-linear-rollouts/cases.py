import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
 r=m.rollout_controls(np.zeros(1),np.ones((1,1)),np.ones((1,1)),np.array([[1.],[2.]]),np.zeros((1,2,1)));assert_array_equal(r['states'],[[[0],[1],[3]]]);assert_array_equal(r['controls'],[[[1],[2]]])
def second(m):
 r=m.rollout_controls(np.zeros(1),np.ones((1,1)),np.ones((1,1)),np.array([[1.],[2.]]),np.array([[[1.],[-1.]]]));assert_array_equal(r['states'],[[[0],[2],[3]]])
def oracle(m):
 rng=np.random.default_rng(810);x=rng.normal(size=16)[::2];a=rng.normal(size=(8,8));a/=2*np.abs(a).sum(axis=1,keepdims=True);b=rng.normal(size=(8,8));u=rng.normal(size=(64,16))[:,::2];eps=rng.normal(size=(128,64,16))[:,:,::2];before=[z.copy() for z in [x,a,b,u,eps]];r=m.rollout_controls(x,a,b,u,eps)
 # Scalar recurrence for independent selected rollouts at full supported dimensions.
 for k in [0,61,127]:
  current=x.tolist();expected=[current]
  for t in range(64):
   current=[sum(float(a[i,j])*current[j] for j in range(8))+sum(float(b[i,j])*(float(u[t,j])+float(eps[k,t,j])) for j in range(8)) for i in range(8)];expected.append(current)
  assert_allclose(r['states'][k],expected,atol=1e-12)
 for z,w in zip(before,[x,a,b,u,eps]):assert_array_equal(z,w)
 assert not np.shares_memory(r['controls'],eps)
def boundaries(m):
 r=m.rollout_controls(np.array([100.]),np.ones((1,1)),np.array([[10.]]),np.array([[100.]]),np.array([[[100.]]]));assert_array_equal(r['states'],[[[100],[2100]]])
def invalid(m):
 for a in [np.array([[1.01]]),np.array([[np.nan]])]:bad(lambda:m.rollout_controls(np.zeros(1),a,np.ones((1,1)),np.ones((1,1)),np.ones((1,1,1))))
 bad(lambda:m.rollout_controls(np.zeros(1),np.eye(1),np.array([[11.]]),np.ones((1,1)),np.ones((1,1,1))))
 bad(lambda:m.rollout_controls(np.zeros(1),np.eye(1),np.ones((1,1)),np.zeros((0,1)),np.zeros((1,0,1))))
 bad(lambda:m.rollout_controls(np.zeros(1),np.eye(1),np.ones((1,1)),np.ones((1,1)),np.ones((1,1,2))))
TESTS=[('Nominal sequence','public',first),('Perturbed sequence','public',second),('Independent scalar rollout at scale','hidden',oracle),('No implicit clipping','hidden',boundaries),('Invalid dynamics contract','hidden',invalid)]
