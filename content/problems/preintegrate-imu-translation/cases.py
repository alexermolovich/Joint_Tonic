import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def call(m,n):return m.preintegrate_translation(np.tile([2.,0,0],(n,1)),np.zeros(3),np.tile(np.eye(3),(n,1,1)),np.full(n,.1))
def first(m):
 r=call(m,1);assert_allclose(r['velocity'],[[0,0,0],[.2,0,0]]);assert_allclose(r['position'],[[0,0,0],[.01,0,0]])
def second(m):
 r=call(m,2);assert_allclose(r['velocity'][-1],[.4,0,0]);assert_allclose(r['position'][-1],[.04,0,0])
def oracle(m):
 rng=np.random.default_rng(828);n=4096;a=rng.normal(size=(n,6))[:,::2];b=np.array([.1,-.2,.3]);rot=np.tile(rz(.7),(n,1,1));dt=np.full(n,1/128);before=[a.copy(),b.copy(),rot.copy(),dt.copy()];out=m.preintegrate_translation(a,b,rot,dt)
 # Direct impulse contribution at selected endpoints, independent of recurrence.
 f=(a-b)@rz(.7).T
 for end in [1,17,1024,4096]:
  expected_v=f[:end].sum(axis=0)/128;weights=(end-np.arange(end)-.5)/128**2;expected_p=(f[:end]*weights[:,None]).sum(axis=0);assert_allclose(out['velocity'][end],expected_v,atol=1e-11);assert_allclose(out['position'][end],expected_p,atol=1e-10)
 for x,y in zip(before,[a,b,rot,dt]):assert_array_equal(x,y)
 assert not np.shares_memory(out['velocity'],a)
def frames(m):
 out=m.preintegrate_translation(np.array([[1.,0,0]]),np.zeros(3),rz(np.pi/2)[None],np.ones(1));assert_allclose(out['velocity'][-1],[0,1,0],atol=1e-12);assert_allclose(out['position'][-1],[0,.5,0],atol=1e-12)
 r=m.preintegrate_translation(np.empty((0,3)),np.zeros(3),np.empty((0,3,3)),np.empty(0));assert_array_equal(r['position'],np.zeros((1,3)))
def invalid(m):
 for a,b,r,t in [(np.zeros((1,3)),np.zeros(3),np.zeros((1,3,3)),np.ones(1)),(np.zeros((1,3)),np.zeros(3),np.eye(3)[None],np.zeros(1)),(np.zeros((1,3)),np.ones(3)*101,np.eye(3)[None],np.ones(1))]:bad(lambda:m.preintegrate_translation(a,b,r,t))
TESTS=[('One force interval','public',first),('Old-velocity position recurrence','public',second),('Independent impulse-sum oracle at scale','hidden',oracle),('Body-frame rotation and empty window','hidden',frames),('Invalid inertial contract','hidden',invalid)]
