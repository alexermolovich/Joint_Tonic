import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.quantize_training_actions([[0],[100]],[[0],[50],[100]],2);assert_allclose(r['lower'],[1]);assert_allclose(r['upper'],[99]);assert_array_equal(r['codes'],[[0],[1],[1]]);assert_allclose(r['decoded'],[[25.5],[74.5],[74.5]])
def empty(m):
    r=m.quantize_training_actions([[0],[100]],np.empty((0,1)),2);assert r['codes'].shape==(0,1);assert r['codes'].dtype==np.int64

def scale(m):
    x=np.repeat(np.arange(10000.)[:,None],16,axis=1)[:,::2];a=np.repeat([[0.],[5000.],[9999.]],8,axis=1);r=m.quantize_training_actions(x,a,256);assert_allclose(r['lower'],99.99);assert_allclose(r['upper'],9899.01);assert np.all(r['codes'][0]==0) and np.all(r['codes'][-1]==255);assert not np.shares_memory(r['decoded'],a)
def invalid(m):
    for a in [([[1],[1]],[[1]],2),([[0],[1]],[[0]],True),([[0],[1]],[[0,1]],2),([[0],[np.nan]],[[0]],2)]:bad(lambda:m.quantize_training_actions(*a))
TESTS=[('Robust uniform bins','public',one),('Empty evaluation actions','public',empty),('Scale training-only bounds','hidden',scale),('Invalid quantizer','hidden',invalid)]
