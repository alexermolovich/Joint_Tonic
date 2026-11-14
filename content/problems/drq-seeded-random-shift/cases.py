import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def constant(m):
    x=np.array([.2,.8]).reshape(1,2,1,1,1);r=m.random_shift(x,1,3);assert_array_equal(r['images'],x);assert_array_equal(r['offsets'],np.random.Generator(np.random.PCG64(3)).integers(0,3,size=(1,2),dtype=np.int64))
def identity(m):
    x=np.arange(8).reshape(1,2,2,2,1)/8;r=m.random_shift(x,0,0);assert_array_equal(r['images'],x);assert_array_equal(r['offsets'],[[0,0]]);assert not np.shares_memory(r['images'],x)
def scale(m):
    x=np.arange(16*4*64*128*3,dtype=float).reshape(16,4,64,128,3)[:,:,:,::2,:];x/=x.max();before=x.copy();state=np.random.get_state();r=m.random_shift(x,8,42);after=np.random.get_state();assert_array_equal(state[1],after[1]);assert state[2:]==after[2:];assert_array_equal(x,before)
    for b,(row,col) in enumerate(r['offsets']):
        rr=np.clip(np.arange(64)+row-8,0,63);cc=np.clip(np.arange(64)+col-8,0,63);assert_array_equal(r['images'][b],x[b][:,rr[:,None],cc[None,:],:])
    assert not np.shares_memory(r['images'],x)
def invalid(m):
    x=np.zeros((1,1,1,1,1))
    for args in [(x,True,1),(x,1,np.int64(1)),(x,1,-1),(x+2,0,0)]:bad(lambda:m.random_shift(*args))
TESTS=[('Temporal shared shift','public',constant),('No padding identity','public',identity),('Scale indexed oracle and RNG isolation','hidden',scale),('Invalid inputs','hidden',invalid)]
