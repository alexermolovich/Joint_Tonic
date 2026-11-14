"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def known(m):np.testing.assert_allclose(m.seeded_episode_noise(np.array([0],dtype=np.int64),0,1,np.zeros(2),np.ones(2)),[[[.1257302210933933,-.1321048632913019]]],rtol=1e-12)
def fixed(m):np.testing.assert_array_equal(m.seeded_episode_noise(np.array([4,8],dtype=np.int64),9,2,np.array([3.]),np.array([0.])),np.full((2,2,1),3.))
def order_rng(m):
 ids=np.array([7,3,19],dtype=np.int64);mean=np.array([1.,2.]);sd=np.array([.1,.2]);np.random.seed(10);expected=np.random.random(4);np.random.seed(10);a=m.seeded_episode_noise(ids,55,9,mean,sd);np.testing.assert_array_equal(np.random.random(4),expected)
 b=m.seeded_episode_noise(ids[::-1],55,9,mean,sd);np.testing.assert_array_equal(a,b[::-1]);single=m.seeded_episode_noise(ids[1:2],55,9,mean,sd);np.testing.assert_array_equal(single[0],a[1]);assert not np.array_equal(a[0],a[1])
def scale_empty(m):
 ids=np.arange(128,dtype=np.int64);mean=np.arange(64,dtype=float)[::2];sd=np.ones(32);r=m.seeded_episode_noise(ids,2**32-1,128,mean,sd);assert r.shape==(128,128,32)
 expected=np.random.Generator(np.random.PCG64(np.random.SeedSequence([2**32-1,127]))).standard_normal((128,32))+mean;np.testing.assert_array_equal(r[-1],expected)
 assert m.seeded_episode_noise(ids[:0],0,3,mean,sd).shape==(0,3,32);assert m.seeded_episode_noise(ids[:1],0,0,mean,sd).shape==(1,0,32);assert not np.shares_memory(r,mean)
def invalid(m):
 good=[np.array([1],dtype=np.int64),0,1,np.zeros(1),np.ones(1)]
 for i,value in [(0,np.array([1,1],dtype=np.int64)),(0,np.array([-1],dtype=np.int64)),(0,np.array([2**32],dtype=np.int64)),(0,np.array([1],dtype=np.int32)),(1,True),(2,257),(3,np.array([np.nan])),(4,np.array([-1.])),(4,np.ones(2))]:
  a=[v.copy() if isinstance(v,np.ndarray) else v for v in good];a[i]=value;rejects(lambda:m.seeded_episode_noise(*a))
 rejects(lambda:m.seeded_episode_noise(np.arange(256,dtype=np.int64),0,256,np.zeros(32),np.ones(32)))

TESTS=[('Known pinned episode stream', 'public', known), ('Fixed sensor channels', 'public', fixed), ('Episode order split replay and global RNG', 'hidden', order_rng), ('Large replay and empty axes', 'hidden', scale_empty), ('Invalid noise schema', 'hidden', invalid)]
