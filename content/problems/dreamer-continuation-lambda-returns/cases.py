import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    assert_allclose(m.imagined_lambda_returns([[1,2]],[[10,20]],[[.5,1]],[[True,True]],.5,1),[[4,12]])

def zero(m):
    assert_allclose(m.imagined_lambda_returns([[1,2]],[[10,20]],[[.5,1]],[[True,True]],.5,0),[[3.5,12]])
    assert m.imagined_lambda_returns([[1,2]],[[10,20]],[[0,1]],[[True,True]],.5,1)[0,0]==1

def oracle(m):
    rng=np.random.default_rng(541);r=rng.normal(size=(64,2048))[:,::2];v=rng.normal(size=r.shape);c=rng.random(r.shape);valid=np.arange(1024)[None]<np.arange(64)[:,None]*16;before=r.copy();out=m.imagined_lambda_returns(r,v,c,valid,.99,.7);expected=np.zeros_like(r)
    for row in range(64):
        length=int(valid[row].sum())
        if not length:continue
        next_return=float(v[row,length-1])
        for t in range(length-1,-1,-1):next_return=float(r[row,t])+.99*float(c[row,t])*(.3*float(v[row,t])+.7*next_return);expected[row,t]=next_return
    assert_allclose(out,expected,atol=1e-12);assert_array_equal(r,before);assert not np.shares_memory(out,r)
    assert_allclose(m.imagined_lambda_returns([[1,2]],[[10,20]],[[.5,1]],[[True,False]],.5,.5),[[3.5,0]])
    assert_allclose(m.imagined_lambda_returns([[1,2]],[[10,20]],[[.5,1]],[[True,True]],.5,.5),[[3.75,12]])

def invalid(m):
    bad(lambda:m.imagined_lambda_returns([[1,2]],[[0,0]],[[1,1]],[[False,True]],1,1));bad(lambda:m.imagined_lambda_returns([[1]],[[0]],[[1.1]],[[True]],1,1));bad(lambda:m.imagined_lambda_returns([[np.nan]],[[0]],[[1]],[[False]],1,1));bad(lambda:m.imagined_lambda_returns([[1]],[[0]],[[1]],[[True]],10**1000,1))
TESTS=[('Fractional predicted continuation','public',one),('One-step targets and termination','public',zero),('Independent reverse scalar oracle prefix boundary and scale','hidden',oracle),('Invalid imagined target contract','hidden',invalid)]
