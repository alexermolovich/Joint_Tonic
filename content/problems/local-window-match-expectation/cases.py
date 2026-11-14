import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def uniform(m):
 r=m.refine_matches(np.zeros((1,1)),np.zeros((1,3,3,1)),np.array([[10.,20.]]),np.ones(2));assert_allclose(r['probabilities'],1/9);assert_allclose(r['offsets'],0,atol=1e-15);assert_allclose(r['refined'],[[10,20]]);assert_allclose(r['covariance'],[np.diag([2/3,2/3])],atol=1e-14)
def peak(m):
 w=np.zeros((1,3,3,1));w[0,1,1,0]=np.log(8);r=m.refine_matches(np.ones((1,1)),w,np.zeros((1,2)),np.ones(2));assert_allclose(r['probabilities'][0,1,1],.5);assert_allclose(r['covariance'],[np.diag([.375,.375])],atol=1e-14)
def oracle(m):
 rng=np.random.default_rng(840);q=rng.normal(size=(64,32))[:,::2];w=rng.normal(size=(64,7,7,32))[:,:,:,::2];centers=rng.normal(size=(64,2));scale=np.array([2.,3.]);before=w.copy();r=m.refine_matches(q,w,centers,scale)
 for b in range(64):
  grid=np.array([[(j-3)*2,(i-3)*3] for i in range(7) for j in range(7)]);logits=np.array([sum(q[b]*w[b,i,j])/4 for i in range(7) for j in range(7)]);p=np.exp(logits-logits.max());p/=sum(p);mean=sum(p[k]*grid[k] for k in range(49));cov=sum(p[k]*np.outer(grid[k]-mean,grid[k]-mean) for k in range(49));assert_allclose(r['offsets'][b],mean,atol=1e-12);assert_allclose(r['covariance'][b],cov,atol=1e-12);assert_allclose(r['refined'][b],centers[b]+mean)
 assert_array_equal(w,before);assert not np.shares_memory(r['probabilities'],w)
def edges(m):
 r=m.refine_matches(np.ones((0,1)),np.ones((0,3,3,1)),np.zeros((0,2)),np.ones(2));assert r['covariance'].shape==(0,2,2)
 r=m.refine_matches(np.ones((1,2)),np.ones((1,1,1,2)),np.array([[2.,3.]]),np.ones(2));assert_array_equal(r['offsets'],[[0,0]]);assert_array_equal(r['covariance'],np.zeros((1,2,2)))
 w=np.zeros((1,3,3,1));w[0,0,0,0]=2;w[0,2,2,0]=2;r=m.refine_matches(np.ones((1,1)),w,np.zeros((1,2)),np.array([2.,3.]));assert r['covariance'][0,0,1]>0
 r=m.refine_matches(np.full((1,64),100.),np.full((1,9,9,64),100.),np.zeros((1,2)),np.ones(2));assert np.isfinite(r['probabilities']).all()
def invalid(m):
 for w,s in [(np.zeros((1,2,2,1)),np.ones(2)),(np.zeros((1,3,3,1)),np.zeros(2)),(np.zeros((1,3,3,1),np.float32),np.ones(2))]:bad(lambda:m.refine_matches(np.ones((1,1)),w,np.zeros((1,2)),s))
TESTS=[('Uniform local expectation','public',uniform),('Concentrated central evidence','public',peak),('Independent local distribution and covariance oracle at scale','hidden',oracle),('Empty singleton correlated axes and stable logits','hidden',edges),('Invalid local windows and scales','hidden',invalid)]
