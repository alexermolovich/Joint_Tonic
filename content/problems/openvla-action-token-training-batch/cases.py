import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.build_action_token_batch([[7],[6,7]],[[8],[9]],0,1,10);assert_array_equal(r['input_ids'],[[7,8,1,0],[6,7,9,1]]);assert_array_equal(r['labels'],[[-100,8,1,-100],[-100,-100,9,1]]);assert_array_equal(r['lengths'],[3,4])
def eos(m):
    r=m.build_action_token_batch([[2]],[[3,4]],0,1,5);assert_array_equal(r['labels'],[[-100,3,4,1]]);assert r['attention_mask'].all()
def scale(m):
    p=np.arange(2,514)[::2];a=np.arange(514,642)[::2];r=m.build_action_token_batch([p]*32,[a]*32,0,1,1000);assert r['input_ids'].shape==(32,321);assert np.all(r['labels'][:,:256]==-100);assert_array_equal(r['labels'][0,256:-1],a);assert not np.shares_memory(r['input_ids'],p)
def invalid(m):
    for a in [([[0]],[[3]],0,1,4),([[2]],[[1]],0,1,4),([[2]],[[3]],0,0,4),([[2.]],[[3]],0,1,4),([np.array([],int)],[[3]],0,1,4)]:bad(lambda:m.build_action_token_batch(*a))
TESTS=[('Padding and prompt exclusion','public',one),('EOS supervision','public',eos),('Scale noncontiguous token streams','hidden',scale),('Invalid batch','hidden',invalid)]
