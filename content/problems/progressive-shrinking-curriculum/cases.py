"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def phases(m):
 for p in range(4):
  r=m.sample_progressive_subnets([4,2],[8,4],[5,3,1],p,4,0)
  u=np.random.Generator(np.random.PCG64(0)).random((4,3));choices=[[4,2] if p>=3 else [4],[8,4] if p>=2 else [8],[5,3,1] if p>=1 else [5]]
  expected=np.array([[a[int(u[i,j]*len(a))] for j,a in enumerate(choices)] for i in range(4)],dtype=np.int64)
  np.testing.assert_array_equal(r,expected)
def empty(m):
 r=m.sample_progressive_subnets([1],[1],[1],0,0,0);assert r.shape==(0,3) and r.dtype==np.int64
def rng(m):
 np.random.seed(5);expected=np.random.random(4);np.random.seed(5)
 a=[8,4,2];r=m.sample_progressive_subnets(a,[16,8],[7,3],3,10000,123);np.testing.assert_array_equal(np.random.random(4),expected)
 assert a==[8,4,2] and r.shape==(10000,3);np.testing.assert_array_equal(r,m.sample_progressive_subnets(a,[16,8],[7,3],3,10000,123))
 assert set(r[:,0])=={8,4,2} and set(r[:,1])=={16,8} and set(r[:,2])=={7,3}
def draw_order(m):
 u=np.random.Generator(np.random.PCG64(7)).random((7,3));r=m.sample_progressive_subnets([1],[1],[9,7,5,3,1],1,7,7)
 np.testing.assert_array_equal(r[:,2],np.array([9,7,5,3,1])[np.floor(u[:,2]*5).astype(int)])
def invalid(m):
 good=[[4,2],[8,4],[5,3],3,2,0]
 for i,value in [(0,[]),(0,[2,4]),(0,[2,2]),(0,[True]),(1,[257]),(2,[4]),(3,4),(4,-1),(4,10001),(5,2**32),(5,True)]:
  args=copy.deepcopy(good);args[i]=value;rejects(lambda:m.sample_progressive_subnets(*args))

TESTS=[('Progressive phase eligibility', 'public', phases), ('Zero samples', 'public', empty), ('Scale determinism and global RNG preservation', 'hidden', rng), ('Fixed axes still consume random columns', 'hidden', draw_order), ('Invalid curriculum settings', 'hidden', invalid)]
