import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.adaptation_step([[2]],[[3]],[[1]],[[2]],[[8]],.1);assert_allclose(r['prediction'],[[10]]);assert r['loss']==4;assert_allclose(r['down'],[[-.6]]);assert_allclose(r['up'],[[1.2]])
def zero(m):
    a=np.ones((1,1));c=np.full((1,1),2.);r=m.adaptation_step([[2]],[[3]],a,c,[[8]],0);assert_array_equal(r['down'],a);assert_array_equal(r['up'],c);assert not np.shares_memory(r['down'],a)
def gradients(m):
    rng=np.random.default_rng(42);x=rng.normal(size=(128,32))[:,::2];w=rng.normal(size=(16,8));a=rng.normal(size=(16,4));c=rng.normal(size=(4,8));y=rng.normal(size=(128,8));old=w.copy();r=m.adaptation_step(x,w,a,c,y,.01);eps=1e-6
    for i,j in [(0,0),(15,3)]:
        ap=a.copy();am=a.copy();ap[i,j]+=eps;am[i,j]-=eps;lp=np.mean((x@w+x@ap@c-y)**2);lm=np.mean((x@w+x@am@c-y)**2);assert_allclose((a-r['down'])[i,j]/.01,(lp-lm)/(2*eps),rtol=1e-5,atol=1e-7)
    cp=c.copy();cm=c.copy();cp[3,7]+=eps;cm[3,7]-=eps;lp=np.mean((x@w+x@a@cp-y)**2);lm=np.mean((x@w+x@a@cm-y)**2);assert_allclose((c-r['up'])[3,7]/.01,(lp-lm)/(2*eps),rtol=1e-5,atol=1e-7)
    assert_array_equal(w,old);assert not np.shares_memory(r['up'],c)
def invalid(m):
    for a in [([[1]],[[1]],[[1]],[[1]],[[1]],-1),([[101]],[[1]],[[1]],[[1]],[[1]],0),([[1]],[[1]],[[1,2]],[[1]],[[1]],0),([[1]],[[1]],[[1]],[[1]],[[1]],True)]:bad(lambda:m.adaptation_step(*a))
TESTS=[('Simultaneous adapter step','public',one),('Zero learning rate','public',zero),('Scale finite differences and freeze','hidden',gradients),('Invalid adapter','hidden',invalid)]
