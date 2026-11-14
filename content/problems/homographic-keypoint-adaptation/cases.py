import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def identity(m):
 p=np.stack([np.full((2,2),.2),np.full((2,2),.8)]);r=m.adapt_keypoints(p,np.tile(np.eye(3),(2,1,1)),np.array([2,2]));assert_allclose(r['probability'],.5);assert_array_equal(r['count'],np.full((2,2),2))
def translation(m):
 h=np.eye(3);h[0,2]=1;r=m.adapt_keypoints(np.array([[[.2,.8]]]),h[None],np.array([1,2]));assert_allclose(r['probability'],[[.8,np.nan]],equal_nan=True);assert_array_equal(r['count'],[[1,0]])
def oracle(m):
 rng=np.random.default_rng(830);p=rng.random((8,48,128))[:,:,::2];before=p.copy();h=np.tile(np.eye(3),(8,1,1));h[:,:2,2]=rng.uniform(-3,3,(8,2));h[:,2,:2]=rng.uniform(-.001,.001,(8,2));r=m.adapt_keypoints(p,h,np.array([32,50]));expected=np.full((32,50),np.nan);counts=np.zeros((32,50),np.int64)
 for y in range(32):
  for x in range(50):
   values=[]
   for j in range(8):
    q=h[j]@np.array([x,y,1]);u,v=q[:2]/q[2]
    if 0<=u<=63 and 0<=v<=47:
     ix=int(np.floor(u));iy=int(np.floor(v));a=u-ix;b=v-iy
     values.append(sum(p[j,min(iy+dy,47),min(ix+dx,63)]*(a if dx else 1-a)*(b if dy else 1-b) for dx in (0,1) for dy in (0,1)))
   counts[y,x]=len(values)
   if values:expected[y,x]=sum(values)/len(values)
 assert_allclose(r['probability'],expected,atol=1e-12,equal_nan=True);assert_array_equal(r['count'],counts);assert_array_equal(p,before);assert not np.shares_memory(r['probability'],p)
def boundaries(m):
 # Invertible matrices with projection denominator exactly the cutoff and just above it.
 h=np.diag([2.,1.,1e-9]);p=np.ones((1,1,1));r=m.adapt_keypoints(p,h[None],np.array([1,1]));assert r['count'][0,0]==0
 h[2,2]=np.nextafter(1e-9,np.inf);r=m.adapt_keypoints(p,h[None],np.array([1,1]));assert r['probability'][0,0]==1
 h=np.eye(3);h[0,2]=.5;r=m.adapt_keypoints(np.array([[[0.,1.]]]),h[None],np.array([1,1]));assert_allclose(r['probability'],[[.5]])
def invalid(m):
 for p,h,s in [(np.ones((1,1,1),np.float32),np.eye(3)[None],np.array([1,1])),(np.ones((1,1,1)),np.zeros((1,3,3)),np.array([1,1])),(np.ones((1,1,1))*2,np.eye(3)[None],np.array([1,1])),(np.ones((1,1,1)),np.eye(3)[None],np.array([0,1]))]:bad(lambda:m.adapt_keypoints(p,h,s))
TESTS=[('Identity aggregation','public',identity),('Unsupported border','public',translation),('Independent projective bilinear oracle at scale','hidden',oracle),('Denominator cutoff and singleton axes','hidden',boundaries),('Malformed maps and warps','hidden',invalid)]
