import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.gate_policy_update([[True,False],[True,True]],[[False]*2]*2,[[False]*2]*2,[[True]*2]*2,1,2,2,0,0);assert r['accepted'];assert_array_equal(r['checks'],[True]*4)
def assisted(m):
    r=m.gate_policy_update([[True,False],[True,True]],[[False]*2]*2,[[False,False],[True,True]],[[True]*2]*2,1,2,2,0,0);assert_array_equal(r['counts'],[2,0]);assert np.isnan(r['success_rate'][1]) and not r['accepted']
def scale(m):
    s=np.ones((2,8192),bool)[:,::2];v=np.zeros_like(s);h=np.zeros_like(s);valid=np.ones_like(s);s[1,::4]=False;v[1,::4]=True;r=m.gate_policy_update(s,v,h,valid,10**9-1,10**9,4096,.25,.25);assert r['accepted'];assert_array_equal(r['success_rate'],[1,.75]);assert_array_equal(r['violation_rate'],[0,.25]);assert not np.shares_memory(r['checks'],s)
    r=m.gate_policy_update(s,v,h,valid,2,2,1,1,1);assert not r['checks'][0]
    zero=np.empty((2,0),bool);r=m.gate_policy_update(zero,zero,zero,zero,0,1,1,1,1);assert np.isnan(r['success_rate']).all();assert_array_equal(r['checks'],[True,False,False,False])
def invalid(m):
    z=np.zeros((2,1),bool)
    for args in [(z,z,z,z,True,1,1,0,0),(z,z,z,z,0,10**1000,1,0,0),(z,z,z,z,0,1,1,np.nan,0),(z.astype(int),z,z,z,0,1,1,0,0)]:bad(lambda:m.gate_policy_update(*args))
TESTS=[('Autonomous improvement gate','public',one),('Assistance cannot improve autonomous evidence','public',assisted),('Inclusive boundaries versions scale and no evidence','hidden',scale),('Invalid release evidence metadata','hidden',invalid)]
