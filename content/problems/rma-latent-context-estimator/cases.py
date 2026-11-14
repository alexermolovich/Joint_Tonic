import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    k=np.zeros((3,1,1));k[1]=3;r=m.estimate_context([[[2]]],[[True]],k,[[4]],[1]);assert_array_equal(r['latent'],[[25]]);assert r['used'][0]
def missing(m):
    k=np.ones((3,1,1));r=m.estimate_context([[[2]]],[[False]],k,[[4]],[1]);assert_array_equal(r['latent'],[[0]]);assert not r['used'][0]
    assert_array_equal(m.estimate_context([[[-2]]],[[True]],k,[[4]],[1])['latent'],[[1]])
def oracle(m):
    rng=np.random.default_rng(531);x=rng.normal(size=(2,4,3));valid=np.array([[False,False,True,True],[True]*4]);k=rng.normal(size=(3,3,2));w=rng.normal(size=(8,2));b=rng.normal(size=2);expected=np.zeros((2,2))
    for bi in range(2):
        values=[]
        for t in range(4):
            for c in range(2):
                total=sum(x[bi,t+offset-1,f]*k[offset,f,c] for offset in range(3) if 0<=t+offset-1<4 and valid[bi,t+offset-1] for f in range(3));values.append(max(total,0) if valid[bi,t] else 0)
        expected[bi]=np.array(values)@w+b
    assert_allclose(m.estimate_context(x,valid,k,w,b)['latent'],expected)
    x=np.ones((32,32,64))[:,:,::2];r=m.estimate_context(x,np.ones((32,32),bool),np.ones((3,32,16)),np.ones((512,16)),np.zeros(16));assert r['latent'].shape==(32,16);assert not np.shares_memory(r['latent'],x)
def invalid(m):
    k=np.ones((3,1,1));bad(lambda:m.estimate_context([[[1],[1]]],[[True,False]],k,np.ones((2,1)),[0]));bad(lambda:m.estimate_context([[[np.nan]]],[[False]],k,[[1]],[0]));bad(lambda:m.estimate_context([[[101]]],[[False]],k,[[1]],[0]))
TESTS=[('Temporal latent inference','public',one),('Missing and negative activation','public',missing),('Scalar temporal oracle and scale','hidden',oracle),('Invalid history and parameters','hidden',invalid)]
