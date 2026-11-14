import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
 r=m.rank_trajectories(np.array([.1,.2,.05]),np.ones(3,bool),np.ones(3,bool),np.array([3.,1,3]),.1);assert_array_equal(r['feasible'],[True,False,True]);assert_array_equal(r['order'],[0,2]);assert r['best']==0
def second(m):
 r=m.rank_trajectories(np.zeros(1),np.zeros(1,bool),np.ones(1,bool),np.zeros(1),0);assert r['best']==-1 and r['order'].shape==(0,)
def empty(m):
 r=m.rank_trajectories(np.empty(0),np.empty(0,bool),np.empty(0,bool),np.empty(0),0);assert r['best']==-1 and r['order'].dtype==np.int64
 r=m.rank_trajectories(np.zeros(2),np.ones(2,bool),np.array([False,True]),np.array([0.,5.]),0);assert_array_equal(r['order'],[1])
def scale(m):
 n=100000;error=np.zeros(n*2)[::2];cost=(np.arange(n*2,dtype=float)%14)[::2];collision=np.arange(n)%3!=0;limits=np.arange(n)%5!=0;before=[x.copy() for x in [error,cost,collision,limits]];r=m.rank_trajectories(error,collision,limits,cost,0)
 expected=sorted((i for i in range(n) if collision[i] and limits[i]),key=lambda i:(cost[i],i));assert_array_equal(r['order'],expected);assert r['best']==expected[0]
 for a,b in zip(before,[error,cost,collision,limits]):assert_array_equal(a,b)
 assert not np.shares_memory(r['feasible'],collision)
def invalid(m):
 for e,c,l,o,t in [(np.array([-1.]),np.ones(1,bool),np.ones(1,bool),np.zeros(1),0),(np.zeros(1),np.ones(1),np.ones(1,bool),np.zeros(1),0),(np.zeros(1),np.ones(1,bool),np.ones(1,bool),np.array([np.inf]),0),(np.zeros(1),np.ones(1,bool),np.ones(1,bool),np.zeros(1),10**1000)]:bad(lambda:m.rank_trajectories(e,c,l,o,t))
TESTS=[('Gated stable ranking','public',first),('No feasible candidate','public',second),('Empty and limit rejection','hidden',empty),('Stable scalar ranking at scale','hidden',scale),('Invalid candidate values','hidden',invalid)]
