import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def identical(m):
    q=np.array([[[1.,0,0,0]]]);v=np.zeros((1,1,3));r=m.imitation_rewards(q,q,v,v);assert_array_equal(r['pose'],[1]);assert_array_equal(r['velocity'],[1]);assert_array_equal(r['angle_error'],[[0]])
def rotated(m):
    r=m.imitation_rewards([[[1,0,0,0]]],[[[0,1,0,0]]],[[[1,0,0]]],[[[0,0,0]]]);assert_allclose(r['angle_error'],[[np.pi]]);assert_allclose(r['pose'],[np.exp(-2*np.pi**2)]);assert_allclose(r['velocity'],[np.exp(-.1)])
def scale(m):
    q=np.tile([1.,0,0,0],(128,32,1));v=np.zeros((128,32,6))[:,:,::2];r=m.imitation_rewards(q,-q,v,v);assert_array_equal(r['pose'],np.ones(128));assert not np.shares_memory(r['angle_error'],q)
    v=np.array([[[1.,0,0],[2,0,0]]]);q=np.tile([1.,0,0,0],(1,2,1));assert_allclose(m.imitation_rewards(q,q,v,np.zeros_like(v))['velocity'],[np.exp(-.5)])
def invalid(m):
    q=np.array([[[1.,0,0,0]]]);v=np.zeros((1,1,3))
    for args in [(q*2,q,v,v),(q,q,np.zeros((1,2,3)),v),(q,q,v+np.inf,v)]:bad(lambda:m.imitation_rewards(*args))
TESTS=[('Matching physical state','public',identical),('Pose and velocity disagreement','public',rotated),('Scale sign invariance and joint sum','hidden',scale),('Invalid motion contract','hidden',invalid)]
