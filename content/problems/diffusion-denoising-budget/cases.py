import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.denoising_budget([1,4,5],2,1,100);assert_array_equal(r['latency_ms'],[3,9,11]);assert_array_equal(r['feasible'],[True,True,False]);assert r['selected_steps']==4
def example2(m):
    r=m.denoising_budget([2,1],5,0,100);assert_array_equal(r['latency_ms'],[10,5]);assert r['feasible'].all() and r['selected_steps']==2
def nofit(m):
    assert m.denoising_budget([1,2],10,1,100)['selected_steps']==0
    s=np.array([3,1,3]);r=m.denoising_budget(s,1,0,100);assert r['selected_steps']==3;assert_array_equal(s,[3,1,3]);assert r['feasible'].dtype==bool
def invalid(m):
    for a in [([],1,0,1),([0],1,0,1),([1.],1,0,1),([1],0,0,1),([1],1,-1,1),([1],1,0,0),([1],True,0,1),([1],1,0,np.nan)]:bad(lambda:m.denoising_budget(*a))
TESTS=[('Deadline budget','public',example1),('Unsorted exact boundary','public',example2),('No feasible candidate and duplicates','hidden',nofit),('Invalid budget inputs','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    s=np.arange(2,258,dtype=np.int64)[::2];copy=s.copy();r=m.denoising_budget(s,.5,2,10)
    assert r['selected_steps']==196;assert_array_equal(s,copy);assert r['latency_ms'].dtype==np.float64 and not np.shares_memory(r['latency_ms'],s)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
