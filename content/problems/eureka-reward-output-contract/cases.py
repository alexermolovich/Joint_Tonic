import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.validate_reward_output([3],[[1,2]],[True],3,0);assert all(r[k][0] for k in ['finite','bounded','consistent','accepted']);assert r['all_valid_accepted'] and r['invalid_count']==0

def missing(m):
    r=m.validate_reward_output([3,np.nan],[[1,1],[0,0]],[True,False],3,0);assert_array_equal(r['consistent'],[False,False]);assert r['invalid_count']==1 and not r['all_valid_accepted']

def limits(m):
    r=m.validate_reward_output([0,3,np.inf],[[4,-4],[1,2],[0,0]],[True]*3,3,0);assert_array_equal(r['bounded'],[False,True,False]);assert_array_equal(r['finite'],[True,True,False])
    r=m.validate_reward_output([1],[[.5,.4]],[True],1,.11);assert r['accepted'][0]
    r=m.validate_reward_output([],np.empty((0,2)),np.empty(0,bool),1,0);assert r['all_valid_accepted'] and r['invalid_count']==0
    c=np.ones((4096,64))[:,::2];before=c.copy();r=m.validate_reward_output(np.full(4096,32.),c,np.ones(4096,bool),32,0);assert r['accepted'].all();assert_array_equal(c,before);assert not np.shares_memory(r['accepted'],c)

def invalid(m):
    for a in [([1],[[1]],[1],1,0),([1e7],[[1]],[True],1,0),([1],[[1]],[True],10**1000,0),([True],[[1]],[True],1,0)]:bad(lambda:m.validate_reward_output(*a))
TESTS=[('Consistent weighted terms','public',one),('Masked nonfinite evidence','public',missing),('Bounds cancellation empty and scale','hidden',limits),('Invalid output metadata','hidden',invalid)]
