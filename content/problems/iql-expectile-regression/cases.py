import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def signed(m):
    r=m.expectile_loss([[2,0]],[[1,1]],[[True,True]],.75);assert r['loss']==.5;assert_array_equal(r['per_element'],[[.75,.25]]);assert_array_equal(r['value_gradient'],[[-.75,.25]])
def empty(m):
    r=m.expectile_loss([[2]],[[0]],[[False]],.7);assert r['loss']==0 and not r['value_gradient'].any()
def scale(m):
    q=np.ones((64,2048))[:,::2]*2;v=np.zeros_like(q);mask=np.ones_like(q,dtype=bool);r=m.expectile_loss(q,v,mask,.8);assert_allclose(r['loss'],3.2);assert_allclose(r['value_gradient'],-3.2/q.size);assert not np.shares_memory(r['per_element'],q)
    eps=1e-6;lp=m.expectile_loss([[2]],[[1+eps]],[[True]],.8)['loss'];lm=m.expectile_loss([[2]],[[1-eps]],[[True]],.8)['loss'];assert_allclose((lp-lm)/(2*eps),-1.6,rtol=1e-6)
def invalid(m):
    for a in [([[1]],[[0]],[[True]],1),([[1]],[[0]],[[1]],.5),([[np.nan]],[[0]],[[False]],.5)]:bad(lambda:m.expectile_loss(*a))
TESTS=[('Asymmetric squared residual','public',signed),('No valid entries','public',empty),('Scale and derivative','hidden',scale),('Invalid expectile inputs','hidden',invalid)]
