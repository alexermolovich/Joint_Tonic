import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.interaction_statistics([10,20],[0,5],[2,3],[True,True],[True,False],[True,True]);assert r['robot_time']==35 and r['human_time']==5 and r['reset_time']==5;assert_allclose(r['human_fraction'],1/6);assert r['reset_success_rate']==.5 and r['autonomous_success_rate']==1 and r['autonomous_trials']==1

def missing(m):
    r=m.interaction_statistics([1],[0],[1],[True],[True],[False]);assert r['trials']==0 and r['robot_time']==0;assert all(np.isnan(r[k]) for k in ['human_fraction','task_success_rate','reset_success_rate','autonomous_success_rate'])

def oracle(m):
    rng=np.random.default_rng(554);t=rng.uniform(1,100,32768)[::2];h=np.where(np.arange(16384)%2,0,t*.25);r=rng.uniform(0,10,16384);s=rng.random(16384)>.3;reset=rng.random(16384)>.1;v=rng.random(16384)>.1;before=t.copy();out=m.interaction_statistics(t,h,r,s,reset,v);ids=[i for i in range(len(t)) if v[i]];auto=[i for i in ids if h[i]==0];assert_allclose(out['robot_time'],sum(float(t[i]+r[i]) for i in ids));assert_allclose(out['human_fraction'],sum(float(h[i]) for i in ids)/sum(float(t[i]) for i in ids));assert_allclose(out['autonomous_success_rate'],sum(bool(s[i]) for i in auto)/len(auto));assert_array_equal(t,before)
    out=m.interaction_statistics([0],[0],[2],[False],[False],[True]);assert out['autonomous_trials']==1 and np.isnan(out['human_fraction']) and out['robot_time']==2
    out=m.interaction_statistics([1],[.1],[0],[True],[True],[True]);assert out['task_success_rate']==1 and np.isnan(out['autonomous_success_rate'])
    out=m.interaction_statistics([],[],[],np.empty(0,bool),np.empty(0,bool),np.empty(0,bool));assert out['trials']==0

def invalid(m):
    for args in [([1],[2],[0],[True],[True],[True]),([-1],[0],[0],[True],[True],[True]),([np.nan],[0],[0],[True],[True],[False]),([1],[0],[0],[1],[True],[True])]:bad(lambda:m.interaction_statistics(*args))
TESTS=[('Human effort and reset overhead','public',one),('Missing observations','public',missing),('Independent time/record oracle scale assisted-only and empty','hidden',oracle),('Invalid even masked durations','hidden',invalid)]
