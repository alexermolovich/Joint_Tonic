import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def diagonal(m):
 r=m.mutual_matches(np.array([[.8,.1,0.],[.2,.7,0.],[0.,0.,0.]]),.5);assert_array_equal(r['pairs'],[[0,0],[1,1]]);assert_array_equal(r['matches_source'],[0,1]);assert_allclose(r['confidence_target'],[.8,.7])
def ties(m):
 r=m.mutual_matches(np.ones((3,3)),0);assert_array_equal(r['pairs'],[[0,0]]);assert_array_equal(r['matches_source'],[0,-1]);assert_array_equal(r['matches_target'],[0,-1]);assert_array_equal(r['confidence_source'],[1,0])
def oracle(m):
 rng=np.random.default_rng(837);p=rng.random((257,770))[:,::2];before=p.copy();r=m.mutual_matches(p,.9);ma=np.full(256,-1);mb=np.full(384,-1);ca=np.zeros(256);cb=np.zeros(384);pairs=[]
 for i in range(256):
  j=max(range(384),key=lambda j:p[i,j]);ii=max(range(256),key=lambda ii:p[ii,j])
  if ii==i and p[i,j]>.9:ma[i]=j;mb[j]=i;ca[i]=p[i,j];cb[j]=p[i,j];pairs.append([i,j])
 assert_array_equal(r['matches_source'],ma);assert_array_equal(r['matches_target'],mb);assert_allclose(r['confidence_source'],ca);assert_allclose(r['confidence_target'],cb);assert_array_equal(r['pairs'],np.array(pairs).reshape(-1,2));assert_array_equal(p,before);assert not np.shares_memory(r['confidence_source'],p)
def boundaries(m):
 r=m.mutual_matches(np.ones((3,3)),1);assert r['pairs'].shape==(0,2)
 for shape in [(1,1),(1,4),(3,1)]:
  r=m.mutual_matches(np.zeros(shape),0);assert r['pairs'].shape==(0,2);assert r['matches_source'].shape==(shape[0]-1,) and r['matches_target'].shape==(shape[1]-1,);assert (r['matches_source']==-1).all() and (r['matches_target']==-1).all()
 r=m.mutual_matches(np.array([[1.,100.],[100.,100.]]),0);assert_array_equal(r['pairs'],[[0,0]])
def invalid(m):
 for p,t in [(np.zeros((0,1)),0),(np.ones((2,2),np.float32),0),(-np.ones((2,2)),0),(np.ones((2,2)),10**1000),(np.ones((2,2)),True)]:bad(lambda:m.mutual_matches(p,t))
TESTS=[('Reciprocal confident pairs','public',diagonal),('First-index exact ties','public',ties),('Independent scalar argmax oracle at scale','hidden',oracle),('Strict threshold empty sides separate dustbin semantics','hidden',boundaries),('Invalid assignment input','hidden',invalid)]
