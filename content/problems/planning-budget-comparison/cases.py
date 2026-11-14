import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
 r=m.compare_budgets(np.array([10,20],dtype=np.int64),np.array([[5.,3],[0,4]]),np.ones((2,2),bool),np.array([[1,1],[0,1]],bool));assert_array_equal(r['counts'],[2,2]);assert_allclose(r['success_rate'],[.5,1]);assert_allclose(r['median_solved_cost'],[5,3.5]);assert_array_equal(r['paired_counts'],[1]);assert_allclose(r['paired_improvement'],[2])
def missing(m):
 r=m.compare_budgets(np.array([10,20],dtype=np.int64),np.zeros((1,2)),np.zeros((1,2),bool),np.zeros((1,2),bool));assert_array_equal(r['counts'],[0,0]);assert np.isnan(r['success_rate']).all() and np.isnan(r['median_solved_cost']).all() and np.isnan(r['paired_improvement']).all()
def scale(m):
 budgets=np.arange(1,257,dtype=np.int64)[::2];costs=np.tile(np.arange(256,0,-1,dtype=float),(256,1))[:,::2];observed=np.ones_like(costs,bool);observed[::3,::4]=False;solved=observed.copy();solved[:30,:3]=False;before=[costs.copy(),observed.copy(),solved.copy()];r=m.compare_budgets(budgets,costs,observed,solved)
 for j in range(128):
  vals=[float(costs[i,j]) for i in range(256) if solved[i,j]];assert_allclose(r['median_solved_cost'][j],np.median(vals));assert_allclose(r['success_rate'][j],len(vals)/sum(bool(observed[i,j]) for i in range(256)))
 assert_allclose(r['paired_improvement'],2)
 for a,b in zip(before,[costs,observed,solved]):assert_array_equal(a,b)
def gaps(m):
 b=np.array([1,2,3],dtype=np.int64);obs=np.array([[True,False,True]]);ok=obs.copy();r=m.compare_budgets(b,np.array([[5.,99,4.]]),obs,ok);assert_array_equal(r['paired_counts'],[0,0]);assert np.isnan(r['paired_improvement']).all()
 bad(lambda:m.compare_budgets(b,np.array([[5.,0,6.]]),obs,ok));bad(lambda:m.compare_budgets(b,np.array([[5.,0,0.]]),obs,np.array([[True,False,False]])))
 r=m.compare_budgets(np.array([1],dtype=np.int64),np.array([[0.]]),np.ones((1,1),bool),np.zeros((1,1),bool));assert r['paired_counts'].shape==(0,) and r['success_rate'][0]==0 and np.isnan(r['median_solved_cost'][0])
def invalid(m):
 bad(lambda:m.compare_budgets(np.array([2,1],dtype=np.int64),np.zeros((1,2)),np.ones((1,2),bool),np.zeros((1,2),bool)))
 bad(lambda:m.compare_budgets(np.array([1],dtype=np.int64),np.zeros((1,1)),np.zeros((1,1),bool),np.ones((1,1),bool)))
 bad(lambda:m.compare_budgets(np.array([1],dtype=np.int64),np.array([[np.nan]]),np.zeros((1,1),bool),np.zeros((1,1),bool)))
TESTS=[('Paired budget comparison','public',first),('Missing observations','public',missing),('Scale and independent column oracle','hidden',scale),('Missing gaps and incumbent consistency','hidden',gaps),('Invalid budget contract','hidden',invalid)]
