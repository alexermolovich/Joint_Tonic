import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def first(m):
 r=m.sphere_collision_cost(np.zeros((1,1,3)),np.ones(1),np.array([[3.,0,0]]),np.ones(1),2);assert_array_equal(r['cost'],[1]);assert_array_equal(r['clearance'],[1]);assert_array_equal(r['collision'],[False])
def contact(m):
 r=m.sphere_collision_cost(np.zeros((1,1,3)),np.ones(1),np.array([[2.,0,0]]),np.ones(1),0);assert r['cost'][0]==0 and r['collision'][0]
def oracle(m):
 rng=np.random.default_rng(3);c=rng.normal(size=(3,4,3));o=rng.normal(size=(5,3));rr=np.linspace(.1,.4,4);ro=np.linspace(.1,.5,5);r=m.sphere_collision_cost(c,rr,o,ro,.2)
 for b in range(3):
  ds=[sum((c[b,i,j]-o[k,j])**2 for j in range(3))**.5-rr[i]-ro[k] for i in range(4) for k in range(5)];assert_allclose(r['cost'][b],sum(max(.2-d,0)**2 for d in ds));assert_allclose(r['clearance'][b],min(ds));assert r['collision'][b]==(min(ds)<=0)
def scale(m):
 c=np.zeros((64,32,6))[:,:,::2];o=np.zeros((32,3));r=m.sphere_collision_cost(c,np.ones(32),o,np.ones(32),0);assert_allclose(r['cost'],4096);assert_allclose(r['clearance'],-2);assert r['collision'].all();assert not np.shares_memory(r['cost'],c)
def invalid(m):
 for rr,margin in [(np.zeros(1),1),(np.ones(1),-1),(np.ones(1),10**1000)]:
  with np.testing.assert_raises(ValueError):m.sphere_collision_cost(np.zeros((1,1,3)),rr,np.zeros((1,3)),np.ones(1),margin)
TESTS=[('Margin before contact','public',first),('Touching at zero margin','public',contact),('Scalar pairwise distance oracle','hidden',oracle),('Coincident noncontiguous batch','hidden',scale),('Invalid geometry contract','hidden',invalid)]
