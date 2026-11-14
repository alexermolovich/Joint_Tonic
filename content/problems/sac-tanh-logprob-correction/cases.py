import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def zero(m):
    r=m.tanh_action_logprob([[0,0]],[-2],[2,3]);assert_array_equal(r['actions'],[[0,0]]);assert_allclose(r['log_prob'],[-2-np.log(6)])
def saturated(m):
    r=m.tanh_action_logprob([[20]],[-1],[1]);assert_allclose(r['log_prob'],[37.6137056389]);assert np.isfinite(r['log_prob']).all()
def scale(m):
    u=np.tile(np.linspace(-100,100,128),(128,1))[:,::2];r=m.tanh_action_logprob(u,np.zeros(128),np.ones(64));assert np.isfinite(r['log_prob']).all();assert np.all(np.abs(r['actions'])<=1);assert not np.shares_memory(r['actions'],u)
    u=np.array([[-.3,.7]]);r=m.tanh_action_logprob(u,[0],[1,2]);assert_allclose(r['log_prob'],-np.log(np.array([1,2])*(1-np.tanh(u)**2)).sum(axis=1))
def invalid(m):
    for a in [([[1]],[0],[0]),([[101]],[0],[1]),([[1]],[0,1],[1]),([[1]],[0],[True])]:bad(lambda:m.tanh_action_logprob(*a))
TESTS=[('Scale determinant','public',zero),('Saturated finite density','public',saturated),('Scale stable Jacobian and direct oracle','hidden',scale),('Invalid action transform','hidden',invalid)]
