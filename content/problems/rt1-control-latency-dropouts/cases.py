import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    r=m.control_latency_report([0,10,20],[5,-1,35],10);assert_array_equal(r['latency_ms'],[5,-1,15]);assert_allclose([r['dropout_rate'],r['deadline_miss_rate'],r['mean_latency_ms']],[1/3,2/3,10])
def example2(m):
    r=m.control_latency_report([2],[-1],4);assert r['mean_latency_ms'] is None and r['dropout_rate']==r['deadline_miss_rate']==1
def boundary(m):
    o=np.array([0,10,20]);a=np.array([10,10,30]);r=m.control_latency_report(o,a,10);assert r['deadline_miss_rate']==0 and r['dropout_rate']==0;assert_allclose(r['mean_latency_ms'],20/3);assert_array_equal(o,[0,10,20]);assert_array_equal(a,[10,10,30])
def invalid(m):
    for o,a,d in [([],[],1),([0,0],[1,1],1),([2],[1],1),([0],[-2],1),([0],[1],0),([0],[1],True),([0],[np.nan],1),([0],[1,2],1)]:bad(lambda:m.control_latency_report(o,a,d))
TESTS=[('Dropout and lateness','public',example1),('No delivered actions','public',example2),('Exact deadline and preservation','hidden',boundary),('Invalid time contract','hidden',invalid)]

# Added realistic scale contract check
def scale_storage(m):
    o=np.arange(20000,dtype=float)[::2];a=o+1;a[::2]=-1;c=o.copy();d=a.copy();r=m.control_latency_report(o,a,1)
    assert r['dropout_rate']==.5 and r['deadline_miss_rate']==.5 and r['mean_latency_ms']==1;assert not np.shares_memory(r['latency_ms'],o);assert_array_equal(o,c);assert_array_equal(a,d)

TESTS.append(('Realistic scale and input preservation','hidden',scale_storage))
