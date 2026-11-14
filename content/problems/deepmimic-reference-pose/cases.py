import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    q=np.array([[[1.,0,0,0]],[[1.,0,0,0]]]);r=m.interpolate_motion([0,2],[[0,0,0],[2,0,0]],q,[1]);assert_array_equal(r['positions'],[[1,0,0]]);assert_array_equal(r['rotations'],q[:1]);assert_array_equal(r['interval'],[0]);assert_array_equal(r['alpha'],[.5])
def signs(m):
    q=np.array([[[1.,0,0,0]],[[-1.,0,0,0]]]);r=m.interpolate_motion([0,2],np.zeros((2,3)),q,[1,3]);assert_array_equal(r['rotations'],np.tile([1.,0,0,0],(2,1,1)));assert_array_equal(r['alpha'],[.5,1])
def arc(m):
    q=np.array([[[1.,0,0,0]],[[0.,0,1,0]]]);r=m.interpolate_motion([0,2],np.zeros((2,3)),q,[1]);assert_allclose(r['rotations'],[[[np.sqrt(.5),0,np.sqrt(.5),0]]]);assert_allclose(np.linalg.norm(r['rotations'],axis=-1),1)
    r=m.interpolate_motion([0,1,3],np.array([[0.,0,0],[1,0,0],[3,0,0]]),np.tile([1.,0,0,0],(3,1,1)),[0,1,2,9]);assert_array_equal(r['interval'],[0,1,1,1]);assert_allclose(r['positions'][:,0],[0,1,2,3])
def scale(m):
    t=np.arange(1024,dtype=float);p=np.zeros((1024,6))[:,::2];q=np.tile([1.,0,0,0],(1024,32,1));r=m.interpolate_motion(t,p,q,np.linspace(0,1023,256));assert r['rotations'].shape==(256,32,4);assert not np.shares_memory(r['positions'],p);assert_array_equal(q[...,0],np.ones((1024,32)))
    r=m.interpolate_motion(t,p,q,[]);assert r['rotations'].shape==(0,32,4)
def invalid(m):
    q=np.tile([1.,0,0,0],(2,1,1))
    for args in [([1,1],np.zeros((2,3)),q,[1]),([0,1],np.zeros((2,3)),q*2,[1]),([0,1],np.zeros((2,3)),q,[-1])]:bad(lambda:m.interpolate_motion(*args))
TESTS=[('Midpoint translation','public',one),('Quaternion signs and clamping','public',signs),('Spherical arc and segment lookup','hidden',arc),('Scale empty queries and independent outputs','hidden',scale),('Invalid motion input','hidden',invalid)]
