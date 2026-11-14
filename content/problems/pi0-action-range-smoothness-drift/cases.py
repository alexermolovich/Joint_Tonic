import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.action_drift([[0],[2],[2]],[0,1,2],[0],[1],[1],[.5]);assert_array_equal(r['range_violation'][:,0],[0,1,1]);assert_array_equal(r['speed_violation'][:,0],[0,1,0]);assert_allclose(r['rate'],[2/3]);assert_allclose(r['drift'],[1/6])
def single(m):
    r=m.action_drift([[1]],[5],[0],[1],[0],[0]);assert r['rate'][0]==0 and not r['speed_violation'].any()
def scale(m):
    a=np.repeat(np.arange(4096.)[:,None],32,axis=1)[:,::2];r=m.action_drift(a,np.arange(4096.),np.zeros(16),np.full(16,4095),np.ones(16),np.zeros(16));assert not r['speed_violation'].any() and not r['range_violation'].any();assert not np.shares_memory(r['rate'],a)
def invalid(m):
    for a in [([[0],[1]],[0,0],[0],[1],[1],[0]),([[0]],[0],[1],[0],[1],[0]),([[0]],[0],[0],[1],[-1],[0]),([[0]],[0],[0],[1],[1],[2])]:bad(lambda:m.action_drift(*a))
TESTS=[('Union rate and drift','public',one),('One sample and inclusive range','public',single),('Scale strided equality speed','hidden',scale),('Invalid monitor','hidden',invalid)]
