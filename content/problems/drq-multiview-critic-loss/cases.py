import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.multiview_critic_loss([[1,3],[4,99]],[0,2],[[True,True],[True,False]]);assert r['loss']==4.5;assert_allclose(r['per_state'],[5,4]);assert_allclose(r['gradient'],[[.5,1.5],[2,0]])
def empty(m):
    r=m.multiview_critic_loss([[1]],[0],[[False]]);assert r['loss']==0 and np.isnan(r['per_state'][0]);assert_array_equal(r['gradient'],[[0]])
def scale(m):
    p=np.ones((128,128))[:,::2]*3;v=np.ones_like(p,dtype=bool);v[::2,1:]=False;y=np.ones(128);r=m.multiview_critic_loss(p,y,v);assert r['loss']==4;assert_allclose(r['gradient'].sum(axis=1),np.full(128,4/128));assert not np.shares_memory(r['gradient'],p)
    h=1e-5;hi=p.copy();lo=p.copy();hi[0,0]+=h;lo[0,0]-=h;assert_allclose((m.multiview_critic_loss(hi,y,v)['loss']-m.multiview_critic_loss(lo,y,v)['loss'])/(2*h),r['gradient'][0,0],atol=1e-8)
def invalid(m):
    for args in [([[1]],[0],[[1]]),([[1]],[0,1],[[True]]),([[np.nan]],[0],[[False]])]:bad(lambda:m.multiview_critic_loss(*args))
TESTS=[('Equal state weighting','public',one),('No observed states','public',empty),('Scale and analytical gradient','hidden',scale),('Invalid inputs','hidden',invalid)]
