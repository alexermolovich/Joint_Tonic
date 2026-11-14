import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def sequence(m):
    r=m.adversarial_style_reward([[-1,0,1,2,3]],[[True]*5]);assert_allclose(r['reward'],[[0,.75,1,.75,0]]);assert_allclose(r['score_gradient'],[[0,.5,0,-.5,0]]);assert r['mean_reward']==.5
def absent(m):
    r=m.adversarial_style_reward([[4,0]],[[True,False]]);assert_array_equal(r['reward'],[[0,0]]);assert_array_equal(r['score_gradient'],[[0,0]])
    assert m.adversarial_style_reward([[0]],[[False]])['mean_reward']==0
def scale(m):
    d=np.linspace(-100,100,128*512).reshape(128,512)[:,::2];r=m.adversarial_style_reward(d,np.ones_like(d,bool));assert ((r['reward']>=0)&(r['reward']<=1)).all();assert not np.shares_memory(r['reward'],d)
    h=1e-5;a=m.adversarial_style_reward([[.3]],[[True]]);hi=m.adversarial_style_reward([[.3+h]],[[True]])['reward'];lo=m.adversarial_style_reward([[.3-h]],[[True]])['reward'];assert_allclose((hi-lo)/(2*h),a['score_gradient'],atol=1e-8)
def invalid(m):
    for args in [([[101]],[[True]]),([[np.nan]],[[False]]),([[1]],[[1]])]:bad(lambda:m.adversarial_style_reward(*args))
TESTS=[('Least-squares reward shape','public',sequence),('Clipped and missing scores','public',absent),('Scale bounded reward and derivative','hidden',scale),('Invalid discriminator scores','hidden',invalid)]
