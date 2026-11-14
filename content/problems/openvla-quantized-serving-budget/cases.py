import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.serving_budget(3,[4,8],[3,3],[4,4],[[2,3],[2,4]],9,3);assert_array_equal(r['weight_bytes'],[2,3]);assert_array_equal(r['total_bytes'],[9,10]);assert_array_equal(r['feasible'],[True,False])
def boundary(m):assert m.serving_budget(2,[4],[0],[0],[[5]],1,5)['feasible'][0]
def scale(m):
    l=np.tile(np.arange(1,8193.),(128,1))[:,::2];r=m.serving_budget(10**12,np.full(128,4),np.zeros(128,int),np.zeros(128,int),l,10**13,1e5);assert np.all(r['weight_bytes']==500000000000);assert np.all(r['p95_latency_ms']==7783);assert r['feasible'].all()
def invalid(m):
    for a in [(True,[4],[0],[0],[[1]],10,1),(3,[3],[0],[0],[[1]],10,1),(3,[4],[-1],[0],[[1]],10,1),(3,[4],[0],[0],[[0]],10,1)]:bad(lambda:m.serving_budget(*a))
TESTS=[('Packed weights and measured latency','public',one),('Inclusive budgets','public',boundary),('Large model and strided measurements','hidden',scale),('Invalid budgets','hidden',invalid)]
