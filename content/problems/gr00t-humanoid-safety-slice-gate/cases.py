import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.humanoid_release_gate([10,10],[9,10],[0,1],[20,10],[True,True],10,.9,20);assert_array_equal(r['slice_pass'],[True,False]);assert r['failures']==[[],['safety_incident']] and not r['release']
def optional(m):assert m.humanoid_release_gate([10,10],[9,10],[0,1],[20,10],[True,False],10,.9,20)['release']
def scale(m):
    n=np.full(256,100,dtype=int)[::2];r=m.humanoid_release_gate(n,n,np.zeros(128,int),np.full(128,20),np.ones(128,bool),100,1,20);assert r['release'] and r['slice_pass'].all()
    r=m.humanoid_release_gate([0,2],[0,0],[0,1],[30,30],[True,True],10,.9,20);assert r['failures']==[['insufficient_trials','latency'],['insufficient_trials','safety_incident','low_success','latency']];assert np.isnan(r['success_rate'][0])
def invalid(m):
    for a in [([1],[2],[0],[1],[True],1,0,1),([1],[1],[0],[1],[False],1,0,1),([1],[1],[2],[1],[True],1,0,1),([1],[1],[0],[1],[True],True,0,1)]:bad(lambda:m.humanoid_release_gate(*a))
TESTS=[('Required incident blocks release','public',one),('Optional failure remains visible','public',optional),('Scale and ordered failure reasons','hidden',scale),('Invalid evidence','hidden',invalid)]
