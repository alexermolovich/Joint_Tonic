import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.distributional_targets([1],[[2,10,4]],[[0,2]],[False],[0,np.log(2),np.log(3)],.5);assert_array_equal(r['bootstrap'],[2]);assert_array_equal(r['td_target'],[2]);assert_allclose(r['reward_targets'],[[0,1,0]]);assert_allclose(r['value_targets'],[[0,0,1]],atol=1e-14)
def terminal(m):
    r=m.distributional_targets([1],[[2,10,4]],[[0,2]],[True],[0,np.log(2),np.log(3)],.5);assert_array_equal(r['td_target'],[1]);assert_array_equal(r['bootstrap'],[2]);assert_array_equal(r['value_targets'],r['reward_targets'])
def selected(m):
    r=m.distributional_targets([0],[[100,-100,4]],[[0,2]],[False],[-1,0,2],1);assert_array_equal(r['bootstrap'],[4]);assert_array_equal(r['td_target'],[4])
    rng=np.random.default_rng(545);q=rng.uniform(-100,100,(1024,32))[:,::2];rewards=rng.uniform(-10,10,1024);idx=np.tile([2,7],(1024,1));done=np.arange(1024)%2==0;before=q.copy();r=m.distributional_targets(rewards,q,idx,done,np.linspace(-10,10,255),.99);target=np.array([rewards[i]+(0 if done[i] else .99*min(q[i,2],q[i,7])) for i in range(1024)]);assert_allclose(r['td_target'],target);assert_allclose(r['value_targets'].sum(axis=-1),1);assert_allclose(r['value_targets']@np.linspace(-10,10,255),np.sign(target)*np.log1p(np.abs(target)),atol=1e-12);assert_array_equal(q,before);assert not np.shares_memory(r['td_target'],q)
    r=m.distributional_targets([],np.empty((0,2)),np.empty((0,2),int),np.empty(0,bool),[-1,1],1);assert r['value_targets'].shape==(0,2)
def invalid(m):
    for idx,q,bins in [([[0,0]],[[1,2]],[-1,1]),([[0,2]],[[1,2]],[-1,1]),([[0,1]],[[1,np.nan]],[-1,1]),([[0,1]],[[1,2]],[0,0])]:bad(lambda:m.distributional_targets([0],q,idx,[True],bins,1))
TESTS=[('Selected critic target and reward bins','public',one),('Terminal reward-only target','public',terminal),('Not all-critic minimum and decoded target invariants at scale','hidden',selected),('Invalid target metadata','hidden',invalid)]
