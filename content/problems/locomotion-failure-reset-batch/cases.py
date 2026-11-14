import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.reset_failed_locomotion([[[1,0,0]],[[0,1.01,0]]],[5,5],5,[[2],[3]],[[0],[1]],[[.2],[.3]],[[.1],[.2]]);assert_array_equal(r['failure'],[False,True]);assert_array_equal(r['timeout'],[False,False]);assert_array_equal(r['state'],[[2],[1]]);assert_allclose(r['last_action'],[[.2],[0]]);assert_allclose(r['feet_air_time'],[[.1],[0]]);assert_array_equal(r['episode_steps'],[5,0])
def timeout(m):
    r=m.reset_failed_locomotion(np.empty((1,0,3)),[6],5,[[2]],[[1]],[[.2]],[[.1]]);assert_array_equal(r['failure'],[False]);assert_array_equal(r['timeout'],[True]);assert_array_equal(r['reset'],[True]);assert_array_equal(r['state'],[[1]])
def oracle(m):
    rng=np.random.default_rng(559);force=rng.normal(scale=.3,size=(4096,16,6))[:,:,::2];ticks=rng.integers(0,20,4096);x=rng.normal(size=(4096,128))[:,::2];initial=np.ones_like(x);actions=rng.uniform(-1,1,(4096,32));air=rng.random((4096,8));before=x.copy();out=m.reset_failed_locomotion(force,ticks,10,x,initial,actions,air)
    failed=np.array([any(sum(float(a)**2 for a in body)**.5>1 for body in env) for env in force]);mask=failed|(ticks>10);assert_array_equal(out['failure'],failed);assert_array_equal(out['reset'],mask)
    for row in range(len(x)):
        assert_array_equal(out['state'][row],initial[row] if mask[row] else x[row]);assert_array_equal(out['last_action'][row],np.zeros(32) if mask[row] else actions[row]);assert_array_equal(out['feet_air_time'][row],np.zeros(8) if mask[row] else air[row])
    assert_array_equal(x,before);assert not np.shares_memory(out['state'],x)
    r=m.reset_failed_locomotion([[[2,0,0]]],[11],10,[[1]],[[0]],[[.1]],[[.1]]);assert r['failure'][0] and r['timeout'][0]
    r=m.reset_failed_locomotion(np.empty((0,0,3)),np.empty(0,int),1,np.empty((0,1)),np.empty((0,1)),np.empty((0,1)),np.empty((0,1)));assert r['state'].shape==(0,1)
def invalid(m):
    for force,limit,action,air in [([[[np.nan,0,0]]],1,[[0]],[[0]]),([[[0,0,0]]],True,[[0]],[[0]]),([[[0,0,0]]],10**1000,[[0]],[[0]]),([[[0,0,0]]],1,[[2]],[[0]]),([[[0,0,0]]],1,[[0]],[[-1]])]:bad(lambda:m.reset_failed_locomotion(force,[0],limit,[[0]],[[0]],action,air))
TESTS=[('Contact threshold and preserved environment','public',one),('Timeout with no selected contact bodies','public',timeout),('Independent contact oracle reset histories scale empty and simultaneous causes','hidden',oracle),('Invalid reset inputs','hidden',invalid)]
