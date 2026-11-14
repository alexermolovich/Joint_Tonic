import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def first(m):
 r=m.bound_trust_step(np.array([.8,-.8]),np.array([.5,-.5]),-np.ones(2),np.ones(2),.3);assert_allclose(r['step'],[.2,-.2]);assert_allclose(r['next_configuration'],[1,-1]);assert_array_equal(r['clipped'],[True,True])
def zero(m):
 r=m.bound_trust_step(np.zeros(1),np.array([.1]),-np.ones(1),np.ones(1),0);assert_array_equal(r['step'],[0]);assert_array_equal(r['clipped'],[True])
def oracle(m):
 q=np.linspace(-1,1,64);p=np.linspace(2,-2,128)[::2];lo=-np.ones(64);hi=np.ones(64);saved=p.copy();r=m.bound_trust_step(q,p,lo,hi,.2)
 for i in range(64):assert_allclose(r['step'][i],max(max(lo[i]-q[i],-.2),min(p[i],min(hi[i]-q[i],.2))))
 assert_array_equal(p,saved);assert not np.shares_memory(r['step'],p);assert_allclose(m.bound_trust_step(q,r['step'],lo,hi,.2)['step'],r['step'])
def invalid(m):
 for q,radius in [(np.array([2.]),.1),(np.zeros(1),-1),(np.zeros(1),10**1000)]:
  with np.testing.assert_raises(ValueError):m.bound_trust_step(q,np.zeros(1),-np.ones(1),np.ones(1),radius)
TESTS=[('Intersect trust and joint bounds','public',first),('Frozen trust region','public',zero),('Scalar projection oracle and idempotence','hidden',oracle),('Invalid current state and radius','hidden',invalid)]
