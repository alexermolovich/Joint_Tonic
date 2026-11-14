import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.assemble_token_groups([[[[1]]],[[[2],[3]]]],[[[True]],[[True,False]]]);assert_array_equal(r['tokens'],[[[1],[2],[0]]]);assert_array_equal(r['offsets'],[0,1,3]);assert_array_equal(r['group_ids'],[0,1,1])
def empty(m):
    r=m.assemble_token_groups([np.empty((1,0,2))]*2,[np.empty((1,0),bool)]*2);assert r['tokens'].shape==(1,0,2);assert_array_equal(r['offsets'],[0,0,0])
def scale(m):
    x=np.arange(8*128*32.).reshape(8,128,32)[:,:,::2];p=np.ones((8,128),bool);p[:,::3]=False;r=m.assemble_token_groups([x]*4,[p]*4);assert r['tokens'].shape==(8,512,16);assert_array_equal(r['tokens'][:,:128],np.where(p[:,:,None],x,0));assert not np.shares_memory(r['tokens'],x)
def invalid(m):
    for x,p in [([],[]),([np.ones((1,2,3))],[np.ones((1,2))]),([np.ones((1,2,3))],[np.ones((1,3),bool)]),([np.full((1,1,1),np.nan)],[np.ones((1,1),bool)])]:bad(lambda:m.assemble_token_groups(x,p))
TESTS=[('Group order and absence','public',one),('Empty groups','public',empty),('Scale and noncontiguous features','hidden',scale),('Invalid groups','hidden',invalid)]
