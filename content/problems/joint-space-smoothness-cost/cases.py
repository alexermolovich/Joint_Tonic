import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def first(m):
 r=m.smoothness_cost(np.array([[0.],[1.],[3.]]),np.array([2.]));assert r['cost']==10;assert_array_equal(r['gradient'],[[-4],[-4],[8]])
def single(m):
 r=m.smoothness_cost(np.array([[7.,-2.]]),np.array([1.,3.]));assert r['cost']==0;assert_array_equal(r['gradient'],[[0,0]])
def derivative(m):
 rng=np.random.default_rng(2);q=rng.normal(size=(5,3));w=np.array([0.,2.,.5]);r=m.smoothness_cost(q,w);e=1e-6
 for i in range(5):
  for j in range(3):
   plus=q.copy();minus=q.copy();plus[i,j]+=e;minus[i,j]-=e;actual=(m.smoothness_cost(plus,w)['cost']-m.smoothness_cost(minus,w)['cost'])/(2*e);assert_allclose(actual,r['gradient'][i,j],atol=1e-7)
 assert_allclose(m.smoothness_cost(q+3,w)['cost'],r['cost'])
def scale(m):
 q=np.arange(4096*32,dtype=float).reshape(4096,32)[:,::2]/100;before=q.copy();w=np.ones(16);r=m.smoothness_cost(q,w);assert_allclose(r['cost'],4095*16*.32**2);assert_allclose(r['gradient'][1:-1],0,atol=1e-11);assert_array_equal(q,before);assert not np.shares_memory(r['gradient'],q)
def invalid(m):
 for q,w in [(np.zeros((0,1)),np.ones(1)),(np.zeros((2,1)),np.array([-1.])),(np.zeros((2,1)),np.ones(2))]:
  with np.testing.assert_raises(ValueError):m.smoothness_cost(q,w)
TESTS=[('Two weighted edges','public',first),('One waypoint','public',single),('Finite difference gradient oracle','hidden',derivative),('Long noncontiguous path','hidden',scale),('Invalid path contract','hidden',invalid)]
