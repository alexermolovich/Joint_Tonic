import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
 r=m.combine_policies(np.array([[[1.]],[[3.]]]),np.array([[2.],[-2.]]));assert_array_equal(r['metric'],[[4]]);assert_array_equal(r['force'],[-4]);assert_array_equal(r['acceleration'],[-1]);assert r['rank']==1
def second(m):
 r=m.combine_policies(np.array([np.diag([1.,0.])]),np.array([[2.,9.]]));assert_array_equal(r['force'],[2,0]);assert_array_equal(r['acceleration'],[2,0]);assert r['rank']==1
def oracle(m):
 rng=np.random.default_rng(818);raw=rng.normal(size=(64,16,16));metrics=raw.transpose(0,2,1)@raw;actions=rng.normal(size=(64,32))[:,::2];before=[metrics.copy(),actions.copy()];r=m.combine_policies(metrics,actions)
 force=sum(metrics[i]@actions[i] for i in range(64));assert_allclose(r['force'],force,rtol=1e-10,atol=1e-10);assert_allclose(r['acceleration'],np.linalg.solve(metrics.sum(axis=0),force),atol=1e-10);assert r['rank']==16
 for x,y in zip(before,[metrics,actions]):assert_array_equal(x,y)
 assert not np.shares_memory(r['acceleration'],actions)
def rank(m):
 r=m.combine_policies(np.zeros((2,3,3)),np.ones((2,3)));assert r['rank']==0;assert_array_equal(r['acceleration'],[0,0,0])
 r=m.combine_policies(np.array([np.diag([1.,1e-10,2e-10])]),np.ones((1,3)));assert r['rank']==2;assert_allclose(r['acceleration'],[1,0,1])
 r=m.combine_policies(np.array([np.diag([-5e-11,1.])]),np.ones((1,2)));assert_allclose(r['metric'],np.diag([0,1]));assert_allclose(r['acceleration'],[0,1])
def invalid(m):
 bad(lambda:m.combine_policies(np.array([[[-1.]]]),np.ones((1,1))))
 bad(lambda:m.combine_policies(np.array([[[1.,.1],[0.,1.]]]),np.ones((1,2))))
 bad(lambda:m.combine_policies(np.empty((0,1,1)),np.empty((0,1))))
 bad(lambda:m.combine_policies(np.zeros((1,2,3)),np.ones((1,2))))
TESTS=[('Competing weighted requests','public',first),('Unsupported direction','public',second),('Independent full-rank solve at scale','hidden',oracle),('Rank cutoff and PSD boundaries','hidden',rank),('Invalid metrics','hidden',invalid)]
