import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.conservative_penalty([[0,0]],[[0]],[True],1);assert_allclose(r['loss'],np.log(2));assert_allclose(r['gradient'],[[-.5,.5]])
def single(m):
    r=m.conservative_penalty([[9]],[[0,0]],[True],2);assert r['loss']==0;assert_array_equal(r['gradient'],[[0]])
def scale(m):
    q=np.full((128,512),10000.)[:,::2];a=np.zeros((128,128),int);v=np.ones(128,bool);r=m.conservative_penalty(q,a,v,2);assert_allclose(r['loss'],2*np.log(256));assert_allclose(r['gradient'].sum(axis=1),0,atol=1e-12);assert not np.shares_memory(r['gradient'],q)
    q=np.array([[1.,-2.,3.],[0.,2.,-1.]]);a=np.array([[0,0,2],[1,2,2]]);v=np.array([True,False]);r=m.conservative_penalty(q,a,v,.7);h=1e-5
    for j in range(3):
        hi=q.copy();lo=q.copy();hi[0,j]+=h;lo[0,j]-=h;fd=(m.conservative_penalty(hi,a,v,.7)['loss']-m.conservative_penalty(lo,a,v,.7)['loss'])/(2*h);assert_allclose(fd,r['gradient'][0,j],atol=1e-8)
    assert m.conservative_penalty(q,a,[False,False],1)['loss']==0
    assert_allclose(m.conservative_penalty(q+100,a,v,.7)['loss'],r['loss'])
def invalid(m):
    for args in [([[0]],[[1]],[True],1),([[0]],[[0]],[1],1),([[np.nan]],[[0]],[False],1),([[0]],[[0]],[True],10**1000)]:bad(lambda:m.conservative_penalty(*args))
TESTS=[('Two action penalty','public',one),('One action cancellation','public',single),('Stable scale duplicates and derivative','hidden',scale),('Invalid inputs','hidden',invalid)]
