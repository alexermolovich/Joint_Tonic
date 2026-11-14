import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def leak(m):
    r=m.offline_split_report([1,1,2],[0,1,2],[0,0,0]);assert_array_equal(r['counts'],[1,1,1]);assert_array_equal(r['leakage_pairs'],[[0,1]]);assert not r['valid']
def scoped(m):assert m.offline_split_report([1,1,1],[0,1,2],[0,1,2])['valid']
def scale(m):
    e=np.arange(200000)[::2];s=np.arange(100000)%3;src=np.zeros(100000,int);r=m.offline_split_report(e,s,src);assert r['valid'] and r['counts'].sum()==100000 and r['leakage_pairs'].shape==(0,2)
    r=m.offline_split_report(np.array([],int),np.array([],int),np.array([],int));assert_array_equal(r['missing_splits'],[0,1,2]);assert not r['valid']
    r=m.offline_split_report([3,2,3,2],[0,0,2,1],[1,0,1,0]);assert_array_equal(r['leakage_pairs'],[[0,2],[1,3]])
def invalid(m):
    for a in [([1.],[0],[0]),([1],[3],[0]),([-1],[0],[0]),([1],[0],[-1])]:bad(lambda:m.offline_split_report(*a))
TESTS=[('Episode leakage','public',leak),('Source-scoped identity','public',scoped),('Scale empty input and sorted report','hidden',scale),('Invalid split IDs','hidden',invalid)]
