import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def active(m):
    r=m.policy_clip_metrics([[np.log(1.5),np.log(.5)]],[[0,0]],[[1,-1]],[[True,True]],.2);assert r['ratio_clip_fraction']==r['active_clip_fraction']==1;assert_allclose(r['approx_kl'],-.5*np.log(.75))
def inactive(m):
    r=m.policy_clip_metrics([[np.log(1.5),np.log(.5)]],[[0,0]],[[-1,1]],[[True,True]],.2);assert r['ratio_clip_fraction']==1 and r['active_clip_fraction']==0

def scale(m):
    x=np.zeros((64,2048))[:,::2];r=m.policy_clip_metrics(x,x,np.ones_like(x),np.ones_like(x,dtype=bool),0);assert r['count']==65536 and r['ratio_clip_fraction']==r['approx_kl']==0
    r=m.policy_clip_metrics([[np.log(2)]],[[0]],[[0]],[[True]],0);assert r['ratio_clip_fraction']==1 and r['active_clip_fraction']==0
    r=m.policy_clip_metrics([[0]],[[0]],[[1]],[[False]],0);assert not any(r.values())
def invalid(m):
    for args in [([[0]],[[101]],[[1]],[[True]],.2),([[0]],[[0]],[[1]],[[1]],.2),([[0]],[[0]],[[1]],[[True]],-1)]:bad(lambda:m.policy_clip_metrics(*args))
TESTS=[('Signed active clipping','public',active),('Excursion without objective clipping','public',inactive),('Scale zero advantage and empty support','hidden',scale),('Invalid diagnostics','hidden',invalid)]
