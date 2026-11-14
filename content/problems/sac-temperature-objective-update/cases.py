import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def high(m):
    r=m.temperature_update(0,[[-2]],[[True]],1,.1);assert r['loss']==r['gradient']==1;assert_allclose(r['log_alpha'],-.1);assert_allclose(r['alpha'],np.exp(-.1))
def low(m):assert_allclose(m.temperature_update(0,[[0]],[[True]],1,.1)['log_alpha'],.1)
def scale(m):
    p=np.full((128,512),-2.)[:,::2];mask=np.ones_like(p,dtype=bool);r=m.temperature_update(1,p,mask,1,0);assert_allclose(r['gradient'],np.e);eps=1e-6;lp=m.temperature_update(1+eps,p,mask,1,0)['loss'];lm=m.temperature_update(1-eps,p,mask,1,0)['loss'];assert_allclose((lp-lm)/(2*eps),r['gradient'],rtol=1e-6)
    assert m.temperature_update(5,[[100]],[[True]],100,1)['log_alpha']==5
    assert m.temperature_update(5,[[-100]],[[True]],-100,1)['log_alpha']==-20

def invalid(m):
    for a in [(0,[[1]],[[False]],0,.1),(6,[[1]],[[True]],0,.1),(0,[[1]],[[True]],0,True)]:bad(lambda:m.temperature_update(*a))
TESTS=[('Entropy above target','public',high),('Entropy below target','public',low),('Scale derivative and bounded update','hidden',scale),('Invalid entropy inputs','hidden',invalid)]
