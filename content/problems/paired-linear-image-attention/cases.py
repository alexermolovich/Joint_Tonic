import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def zero(m):
 a=np.array([[1.,2.],[3.,4.]]);b=np.array([[5.,6.]]);r=m.paired_attention(a,b,np.zeros((4,2,2)),np.array([True,False]),np.ones(1,bool));assert_array_equal(r['source'],[[1,2],[0,0]]);assert_array_equal(r['target'],b)
def simultaneous(m):
 r=m.paired_attention(np.array([[1.]]),np.array([[2.]]),np.ones((4,1,1)),np.ones(1,bool),np.ones(1,bool));assert_allclose(r['self_source'],[[2]]);assert_allclose(r['self_target'],[[4]]);assert_allclose(r['source'],[[6]]);assert_allclose(r['target'],[[6]])
def oracle(m):
 rng=np.random.default_rng(838);a=rng.normal(size=(96,16))[:,::2];b=rng.normal(size=(128,16))[:,::2];w=rng.normal(scale=.2,size=(4,8,8));ma=rng.random(96)>.2;mb=rng.random(128)>.2;before=a.copy();r=m.paired_attention(a,b,w,ma,mb)
 # Independent explicit pairwise positive-kernel attention, not K.T@V factorization.
 def msg(x,y,mx,my):
  q=x@w[0];k=y@w[1];q=np.where(q>=0,q+1,np.exp(np.minimum(q,0)));k=np.where(k>=0,k+1,np.exp(np.minimum(k,0)));scores=q@k.T;scores[:,~my]=0;values=y@w[2];out=np.zeros_like(x)
  for i in range(len(x)):
   if mx[i]:out[i]=sum((scores[i,j]*values[j] for j in range(len(y))),np.zeros(8))/max(sum(scores[i]),1e-9)@w[3]
  return out
 a0=np.where(ma[:,None],a,0);b0=np.where(mb[:,None],b,0);a1=a0+msg(a0,a0,ma,ma);b1=b0+msg(b0,b0,mb,mb)
 assert_allclose(r['self_source'],a1,atol=1e-12);assert_allclose(r['source'],a1+msg(a1,b1,ma,mb),atol=1e-12);assert_allclose(r['target'],b1+msg(b1,a1,mb,ma),atol=1e-12);assert_array_equal(a,before);assert not np.shares_memory(r['source'],a)
def edges(m):
 for a,b,ma,mb in [(np.empty((0,2)),np.ones((1,2)),np.empty(0,bool),np.ones(1,bool)),(np.ones((1,2)),np.ones((1,2)),np.ones(1,bool),np.zeros(1,bool))]:
  r=m.paired_attention(a,b,np.tile(np.eye(2),(4,1,1)),ma,mb);assert_allclose(r['source'],r['self_source']);assert r['target'].shape==b.shape
 with np.errstate(over='raise',invalid='raise'):
  r=m.paired_attention(np.full((256,32),10.),np.full((256,32),10.),np.full((4,32,32),2.),np.ones(256,bool),np.ones(256,bool));assert np.isfinite(r['source']).all()
 # Tiny positive features test explicit denominator floor.
 w=np.ones((4,1,1));w[0]=-2;w[1]=-2;r=m.paired_attention(np.array([[10.]]),np.empty((0,1)),w,np.ones(1,bool),np.empty(0,bool));assert r['self_source'][0,0]<10.000001
def invalid(m):
 for a,w,mask in [(np.ones((1,1),np.float32),np.ones((4,1,1)),np.ones(1,bool)),(np.ones((1,1)),np.ones((4,1,1))*3,np.ones(1,bool)),(np.ones((1,1)),np.ones((4,1,1)),np.ones(1))]:bad(lambda:m.paired_attention(a,np.ones((1,1)),w,mask,np.ones(1,bool)))
TESTS=[('Zero message weights','public',zero),('Simultaneous cross residuals','public',simultaneous),('Independent pairwise kernel oracle at scale','hidden',oracle),('Empty context masks denominator floor overflow stability','hidden',edges),('Invalid attention shape weights and masks','hidden',invalid)]
