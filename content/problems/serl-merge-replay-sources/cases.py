import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def pool(ids,rewards=None):
    n=len(ids);return {'ids':np.array(ids,dtype=np.int64),'observations':np.zeros((n,1)),'actions':np.zeros((n,1)),'rewards':np.array(rewards if rewards is not None else [0]*n,dtype=float),'next_observations':np.ones((n,1)),'terminated':np.zeros(n,bool)}
def one(m):
    r=m.merge_replay(pool([2],[1]),pool([1],[2]));assert_array_equal(r['ids'],[1,2]);assert_array_equal(r['rewards'],[2,1]);assert_array_equal(r['origin'],[2,1])
def duplicate(m):
    r=m.merge_replay(pool([5]),pool([5]));assert_array_equal(r['ids'],[5]);assert_array_equal(r['origin'],[3]);a=pool([5]);a['actions'][0]=1;bad(lambda:m.merge_replay(pool([5]),a))
def scale(m):
    a=pool(list(range(0,8192,2)));b=pool(list(range(1,8192,2)));a['observations']=np.zeros((4096,32))[:,::2];a['next_observations']=np.ones((4096,16));b['observations']=np.zeros((4096,16));b['next_observations']=np.ones((4096,16));before=a['ids'].copy();r=m.merge_replay(a,b);assert_array_equal(r['ids'],np.arange(8192));assert_array_equal(r['origin'],np.tile([1,2],4096));assert_array_equal(a['ids'],before);assert not np.shares_memory(r['observations'],a['observations']);assert r['ids'].dtype==np.int64
    r=m.merge_replay(pool([]),pool([]));assert r['observations'].shape==(0,1) and r['origin'].dtype==np.int64
    # Storage provenance is merged without assuming online means autonomous.
    a=pool([1]);b=pool([1]);a['actions'][0]=b['actions'][0]=.7;assert m.merge_replay(a,b)['actions'][0,0]==.7

def invalid(m):
    for key,value in [('ids',np.array([1,1])),('terminated',np.array([1])),('next_observations',np.zeros((1,2))),('rewards',np.array([np.nan]))]:
        a=pool([1]);a[key]=value;bad(lambda:m.merge_replay(a,pool([])))
    a=pool([1]);a['extra']=1;bad(lambda:m.merge_replay(a,pool([])))
TESTS=[('Sorted source union','public',one),('Duplicate provenance and conflict rejection','public',duplicate),('Noncontiguous full source scale empty and action preservation','hidden',scale),('Invalid replay identity/schema','hidden',invalid)]
