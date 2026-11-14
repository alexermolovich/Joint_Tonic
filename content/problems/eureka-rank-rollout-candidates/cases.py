import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.rank_reward_candidates([[True,False],[True,True]],[[False]*2]*2,[[True]*2]*2,2,0);assert_array_equal(r['order'],[1,0]);assert r['selected']==1

def safety(m):
    r=m.rank_reward_candidates([[True,False],[True,True]],[[False,False],[True,False]],[[True]*2]*2,2,0);assert_array_equal(r['order'],[0]);assert r['selected']==0

def ties(m):
    s=np.ones((4,4),bool);v=np.zeros_like(s);valid=s.copy();valid[0,2:]=False;v[3,0]=True;r=m.rank_reward_candidates(s,v,valid,1,.25);assert_array_equal(r['order'],[1,2,0,3]);assert r['eligible'].all()
    r=m.rank_reward_candidates(np.empty((1,0),bool),np.empty((1,0),bool),np.empty((1,0),bool),1,1);assert r['selected']==-1 and np.isnan(r['success_rate']).all()
    rng=np.random.default_rng(536);s=rng.random((128,8192))[:,::2]>.4;v=rng.random(s.shape)>.9;valid=rng.random(s.shape)>.1;before=s.copy();r=m.rank_reward_candidates(s,v,valid,1,1);expected=[]
    for k in range(128):
        ids=[j for j in range(4096) if valid[k,j]];sr=sum(bool(s[k,j]) for j in ids)/len(ids);vr=sum(bool(v[k,j]) for j in ids)/len(ids);expected.append((-sr,vr,-len(ids),k))
    assert_array_equal(r['order'],[a[-1] for a in sorted(expected)]);assert_array_equal(s,before);assert not np.shares_memory(r['eligible'],s)

def invalid(m):
    bad(lambda:m.rank_reward_candidates([[1]],[[False]],[[True]],1,0));bad(lambda:m.rank_reward_candidates([[True]],[[False]],[[True]],True,0));bad(lambda:m.rank_reward_candidates([[True]],[[False]],[[True]],1,10**1000))
TESTS=[('Independent success ranking','public',one),('Safety evidence gate','public',safety),('Exact ties missing data and scale oracle','hidden',ties),('Invalid rollout labels','hidden',invalid)]
