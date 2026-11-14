import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
 r=m.assemble_residuals(np.array([2.]),np.array([.1,.5]),.3,.2);assert_allclose(r['residual'],[2,1,0]);assert_allclose([r['prior_cost'],r['obstacle_cost'],r['total_cost']],[2,.5,2.5])
def second(m):
 r=m.assemble_residuals(np.empty(0),np.array([-.1]),0,.1);assert_allclose(r['residual'],[1]);assert_allclose(r['total_cost'],.5)
def empty(m):
 r=m.assemble_residuals(np.empty(0),np.empty(0),1,1);assert r['residual'].shape==(0,) and r['total_cost']==0
 r=m.assemble_residuals(np.array([-2.]),np.array([.5]),.5,1);assert_array_equal(r['residual'],[-2,0])
def scale(m):
 p=np.linspace(-1,1,131072)[::2];d=np.linspace(-2,2,131072)[::2];before=[p.copy(),d.copy()];r=m.assemble_residuals(p,d,.2,.4)
 expected=np.array([max(.2-float(v),0)/.4 for v in d]);assert_allclose(r['residual'][len(p):],expected);assert_allclose(r['total_cost'],.5*sum(float(v)**2 for v in p)+.5*sum(float(v)**2 for v in expected));assert not np.shares_memory(r['residual'],p)
 for x,y in zip(before,[p,d]):assert_array_equal(x,y)
def invalid(m):
 for s in [0,1e-7,True,float('nan'),10**1000]:bad(lambda:m.assemble_residuals(np.zeros(1),np.zeros(1),0,s))
 bad(lambda:m.assemble_residuals(np.zeros(65537),np.zeros(1),0,1));bad(lambda:m.assemble_residuals(np.array([np.inf]),np.zeros(1),0,1))
TESTS=[('Prior plus clearance factor','public',first),('Penetration factor','public',second),('Empty factors and margin equality','hidden',empty),('Scale scalar oracle and preservation','hidden',scale),('Invalid factors','hidden',invalid)]
