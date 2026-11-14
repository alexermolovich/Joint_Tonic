import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def first(m):
 r=m.integrate_jerk(np.zeros(1),np.zeros(1),np.zeros(1),np.array([2.]),.5);assert_allclose(r['position'],[1/24]);assert_allclose(r['velocity'],[.25]);assert_allclose(r['acceleration'],[1])
def zero(m):
 q=np.array([1.]);r=m.integrate_jerk(q,np.array([2.]),np.array([3.]),np.array([4.]),0);assert_array_equal(r['position'],q);assert not np.shares_memory(r['position'],q)
def composition(m):
 q=np.array([.3,-.4]);v=np.array([.2,.7]);a=np.array([-.2,.1]);j=np.array([.9,-.8]);r=m.integrate_jerk(q,v,a,j,.2);s=m.integrate_jerk(r['position'],r['velocity'],r['acceleration'],j,.3);t=m.integrate_jerk(q,v,a,j,.5)
 for k in s:assert_allclose(s[k],t[k],atol=1e-12)
def invalid(m):
 for t in [-1,101,True,10**1000]:
  with np.testing.assert_raises(ValueError):m.integrate_jerk(np.zeros(1),np.zeros(1),np.zeros(1),np.zeros(1),t)
 with np.testing.assert_raises(ValueError):m.integrate_jerk(np.zeros(2),np.zeros(1),np.zeros(2),np.zeros(2),1)
def scale(m):
 q=np.arange(128,dtype=float)[::2];before=q.copy();r=m.integrate_jerk(q,q,q,q,1);assert_allclose(r['position'],q*(1+1+.5+1/6));assert_array_equal(q,before)
 for x in r.values():assert not np.shares_memory(x,q)
TESTS=[('Cubic segment','public',first),('Zero duration','public',zero),('Segment composition oracle','hidden',composition),('Invalid contracts','hidden',invalid),('Noncontiguous joint batch','hidden',scale)]
