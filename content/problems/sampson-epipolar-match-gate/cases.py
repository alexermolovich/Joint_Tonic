import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

F=np.array([[0.,0.,0.],[0.,0.,-1.],[0.,1.,0.]])
def offset(m):
 r=m.epipolar_gate(np.zeros((1,2)),np.array([[3.,2.]]),F,np.ones(1,bool),np.sqrt(2).item());assert_allclose(r['squared_error'],[2]);assert r['accepted'][0]
def aligned(m):
 r=m.epipolar_gate(np.zeros((1,2)),np.array([[3.,0.]]),F,np.ones(1,bool),0);assert r['squared_error'][0]==0 and r['accepted'][0]
def oracle(m):
 rng=np.random.default_rng(841);a=rng.normal(size=(8192,4))[:,::2];b=rng.normal(size=(8192,4))[:,::2];u,_,v=np.linalg.svd(rng.normal(size=(3,3)));f=u@np.diag([2.,1.,0.])@v;mask=rng.random(8192)>.2;before=a.copy();r=m.epipolar_gate(a,b,f,mask,.5);f/=np.linalg.norm(f);expected=[]
 for i in range(8192):
  aa=np.r_[a[i],1.];bb=np.r_[b[i],1.];lb=f@aa;la=f.T@bb;den=lb[0]**2+lb[1]**2+la[0]**2+la[1]**2;expected.append(float(bb@lb)**2/den if mask[i] and den>1e-12 else np.inf)
 assert_allclose(r['squared_error'],expected);assert_array_equal(r['accepted'],np.array(expected)<=.25);assert_array_equal(a,before);assert not np.shares_memory(r['squared_error'],a)
def edges(m):
 for factor in [1.,-5.,1e-200,-1e-300]:
  r=m.epipolar_gate(np.zeros((1,2)),np.array([[3.,2.]]),F*factor,np.ones(1,bool),1);assert_allclose(r['squared_error'],[2]);assert not r['accepted'][0]
 f=np.diag([1.,1.,0.]);r=m.epipolar_gate(np.zeros((1,2)),np.zeros((1,2)),f,np.ones(1,bool),1);assert np.isinf(r['squared_error'][0]) and not r['accepted'][0]
 r=m.epipolar_gate(np.array([[1e-7,0.]]),np.zeros((1,2)),f,np.ones(1,bool),1);assert np.isinf(r['squared_error'][0])
 r=m.epipolar_gate(np.zeros((1,2)),np.zeros((1,2)),F,np.zeros(1,bool),1);assert np.isinf(r['squared_error'][0])
 r=m.epipolar_gate(np.empty((0,2)),np.empty((0,2)),F,np.empty(0,bool),0);assert r['squared_error'].shape==(0,)
def invalid(m):
 for f,t in [(np.zeros((3,3)),0),(np.eye(3),0),(np.diag([1.,0.,0.]),0),(F,10**1000),(F,True)]:bad(lambda:m.epipolar_gate(np.zeros((1,2)),np.zeros((1,2)),f,np.ones(1,bool),t))
TESTS=[('Inclusive geometric threshold','public',offset),('Aligned correspondence','public',aligned),('Independent scalar epipolar oracle at scale','hidden',oracle),('Tiny and negative matrix scales degeneracy masks empty','hidden',edges),('Invalid matrix rank and threshold','hidden',invalid)]
