"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import math
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')

def same(a,b):np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)
def f(x):return np.array(x,dtype=np.float64)
def i(x):return np.array(x,dtype=np.int64)
def b(x):return np.array(x,dtype=bool)

def unchanged(before,after):
    for x,y in zip(before,after):np.testing.assert_array_equal(x,y)

def run(m,r,e,x,n):return m.cross_robot_prediction_error(i(r),i(e),f(x),i(n))
def example1(m):
 r=run(m,[0,0],[1,2],[1,0],[1,9]);same(r['episode_counts'],[2]);same(r['pixel_counts'],[10]);same(r['pixel_mse'],[.1]);same(r['episode_mse'],[.5])
def example2(m):
 r=run(m,[2],[8],[0],[0]);same(r['robot_ids'],[2]);same(r['episode_counts'],[0]);same(r['pixel_counts'],[0]);assert np.isnan(r['pixel_mse']).all() and np.isnan(r['episode_mse']).all()
def edges(m):
 r=run(m,[0,0,1],[7,7,7],[1,0,3],[1,9,3]);same(r['episode_counts'],[1,1]);same(r['episode_mse'],[.1,1])
 r=run(m,[],[],[],[]);assert r['pixel_mse'].shape==(0,) and r['robot_ids'].dtype==np.int64
 hi=2**63-1;r=run(m,[hi,hi-1],[hi,hi],[0,1],[1,1]);np.testing.assert_array_equal(r['robot_ids'],[hi-1,hi]);same(r['pixel_mse'],[1,0])
 a=[i([0,0,1])[::-1],i([7,7,7])[::-1],f([1,0,3])[::-1],i([1,9,3])[::-1]];before=[v.copy() for v in a];r=m.cross_robot_prediction_error(*a);same(r['pixel_mse'],[.1,1]);same(r['episode_mse'],[.1,1]);unchanged(before,a)
 assert all(not np.shares_memory(out,x) for out in r.values() for x in a)
def oracle_scale(m):
 n=100000;robots=np.arange(n,dtype=np.int64)%5;episodes=np.arange(n,dtype=np.int64)%100;counts=np.ones(n,dtype=np.int64)*1000000000;error=np.ones(n)*250000000;before=[x.copy() for x in [robots,episodes,error,counts]];r=m.cross_robot_prediction_error(robots,episodes,error,counts);same(r['episode_counts'],[20]*5);same(r['pixel_counts'],[20000000000000]*5);same(r['pixel_mse'],[.25]*5);same(r['episode_mse'],[.25]*5);unchanged(before,[robots,episodes,error,counts])
def invalid(m):
 for r,e,x,n in [([-1],[0],[0],[1]),([0],[-1],[0],[1]),([0],[0],[1],[0]),([0],[0],[np.nan],[1]),([0],[0],[2],[1]),([0],[0],[0],[-1]),([0],[],[0],[1])]:reject(lambda:run(m,r,e,x,n))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
