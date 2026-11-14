import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def first(m):
 r=m.choose_tree_parent(np.array([3.,1.,2.]),np.array([1.,4.,2.]),np.ones(3,bool));assert r==dict(parent=0,total_cost=4.)
def none(m):
 r=m.choose_tree_parent(np.array([0.,5.]),np.array([0.,1.]),np.zeros(2,bool));assert r['parent']==-1 and np.isposinf(r['total_cost'])
def oracle(m):
 rng=np.random.default_rng(9);a=rng.random(200);b=rng.random(200);valid=rng.random(200)>.5;r=m.choose_tree_parent(a,b,valid);best=min((a[i]+b[i],i) for i in range(200) if valid[i]);assert r['parent']==best[1];assert_allclose(r['total_cost'],best[0]);r=m.choose_tree_parent(np.empty(0),np.empty(0),np.empty(0,bool));assert r['parent']==-1 and np.isposinf(r['total_cost'])
def scale(m):
 a=np.arange(200000,dtype=float)[::2];b=np.zeros(100000);v=np.zeros(100000,bool);v[-1]=True;saved=a.copy();r=m.choose_tree_parent(a,b,v);assert r['parent']==99999 and r['total_cost']==199998;assert_array_equal(a,saved)
def invalid(m):
 for a,b,v in [(np.array([-1.]),np.zeros(1),np.ones(1,bool)),(np.ones(1),np.ones(2),np.ones(1,bool)),(np.ones(1),np.ones(1),np.ones(1,np.int64))]:
  with np.testing.assert_raises(ValueError):m.choose_tree_parent(a,b,v)
TESTS=[('Cumulative cost and exact tie','public',first),('No feasible parent','public',none),('Independent selection and empty support','hidden',oracle),('Large strided cost vector','hidden',scale),('Invalid candidate costs','hidden',invalid)]
