import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def uniform(m):
    r=m.update_elite_distribution([[[-1]],[[1]]],[0,0],[True,True],2,1,0,2);assert_array_equal(r['weights'],[.5,.5]);assert_array_equal(r['mean'],[[0]]);assert_array_equal(r['std'],[[1]])
def weighted(m):
    r=m.update_elite_distribution([[[-1]],[[1]]],[0,np.log(3)],[True,True],2,1,0,2);assert_array_equal(r['elite_indices'],[1,0]);assert_allclose(r['weights'],[.75,.25]);assert_allclose(r['mean'],[[.5]]);assert_allclose(r['std'],[[np.sqrt(.75)]])
    assert m.update_elite_distribution([[[-1]],[[1]]],[0,np.log(3)],[True,True],2,1,0,.5)['std'][0,0]==.5
def oracle(m):
    rng=np.random.default_rng(547);a=rng.uniform(-1,1,(512,32,64))[:,:,::2];s=rng.uniform(-10,10,512);v=rng.random(512)>.3;before=a.copy();r=m.update_elite_distribution(a,s,v,32,.5,.05,1);ids=sorted([i for i in range(512) if v[i]],key=lambda i:(-s[i],i))[:32];w=np.array([np.exp(.5*(s[i]-s[ids[0]])) for i in ids]);w/=w.sum();mean=sum(w[j]*a[i] for j,i in enumerate(ids));std=np.sqrt(sum(w[j]*(a[i]-mean)**2 for j,i in enumerate(ids)));assert_array_equal(r['elite_indices'],ids);assert_allclose(r['mean'],mean);assert_allclose(r['std'],np.clip(std,.05,1));assert_array_equal(a,before);assert not np.shares_memory(r['mean'],a)
    r=m.update_elite_distribution([[[-1]],[[0]],[[1]]],[10,0,0],[False,True,True],2,0,.2,1);assert_array_equal(r['elite_indices'],[1,2]);assert_array_equal(r['weights'],[.5,.5]);assert_array_equal(r['mean'],[[.5]])
    r=m.update_elite_distribution([[[1]]],[1],[True],1,100,.1,1);assert_array_equal(r['std'],[[.1]])
def invalid(m):
    for a,s,v,n,beta,lo,hi in [([[[0]]],[0],[False],1,1,0,1),([[[0]]],[0],[True],True,1,0,1),([[[0]]],[0],[True],1,1,1,0),([[[0]]],[0],[True],1,10**1000,0,1),([[[np.nan]]],[0],[False],1,1,0,1)]:bad(lambda:m.update_elite_distribution(a,s,v,n,beta,lo,hi))
TESTS=[('Equal-score proposal','public',uniform),('Weighted variance and clamping','public',weighted),('Independent weighted oracle invalid candidate exclusion ties and scale','hidden',oracle),('Invalid planner envelope','hidden',invalid)]
