import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.mix_corrective_replay([[.1],[.2],[.3],[.4]],[True,False,True,False],[.8,.4,.1,.2],2,.5);assert_array_equal(r['indices'],[2,3]);assert_allclose(r['actions'],[[.3],[.4]]);assert_array_equal(r['counts'],[1,1])
def round_up(m):
    r=m.mix_corrective_replay([[0],[1]],[False,True],[.1,.5],1,.5);assert_array_equal(r['indices'],[1]);bad(lambda:m.mix_corrective_replay([[0]],[False],[.1],1,.5))
def oracle(m):
    rng=np.random.default_rng(552);a=rng.uniform(-1,1,(16384,32))[:,::2];human=np.arange(16384)%2==0;p=rng.random(16384);before=a.copy();r=m.mix_corrective_replay(a,human,p,4096,.25);expected=sorted(np.flatnonzero(human),key=lambda i:(p[i],i))[:1024]+sorted(np.flatnonzero(~human),key=lambda i:(p[i],i))[:3072];assert_array_equal(r['indices'],expected);assert_array_equal(r['actions'],a[expected]);assert len(set(r['indices']))==4096;assert_array_equal(a,before);assert not np.shares_memory(r['actions'],a)
    r=m.mix_corrective_replay([[0],[1]],[True,True],[.5,.5],1,1);assert_array_equal(r['indices'],[0])
    r=m.mix_corrective_replay(np.empty((0,1)),np.empty(0,bool),np.empty(0),0,.5);assert r['actions'].shape==(0,1)

def invalid(m):
    for args in [([[0]],[True],[1.],1,1),([[0]],[True],[.1],True,1),([[2]],[True],[.1],0,1),([[0]],[True],[np.nan],0,1)]:bad(lambda:m.mix_corrective_replay(*args))
TESTS=[('Source-exclusive corrective sample','public',one),('Half-up quota and no fallback','public',round_up),('Independent priority order no replacement ties and scale','hidden',oracle),('Invalid source sampling contract','hidden',invalid)]
