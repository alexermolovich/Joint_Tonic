import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def solved(m):
    q,ok,e=m.solve_planar_ik([1,1],[0,np.pi/2],[1,1],20,1e-6,.5); assert ok is True and len(e)==1; assert_allclose(q,[0,np.pi/2])
def unreachable(m):
    q,ok,e=m.solve_planar_ik([1,1],[0,0],[3,0],2,1e-6,.5); assert ok is False; assert_allclose(q,0,atol=1e-9); assert_allclose(e,[1,1,1])
def reachable(m):
    initial=np.array([.3,.5]); old=initial.copy(); q,ok,e=m.solve_planar_ik([1,1],initial,[1,1],100,1e-8,.3)
    assert ok and e[-1]<=1e-8; position=[np.cos(q[0])+np.cos(q.sum()),np.sin(q[0])+np.sin(q.sum())]; assert_allclose(position,[1,1],atol=1e-8); assert_array_equal(initial,old)
def exact_update(m):
    start=np.array([0.,np.pi/2]); q,ok,e=m.solve_planar_ik([1,1],start,[1.2,1.1],1,1e-12,1)
    # At this pose J=[[-1,-1],[1,0]], so delta=[0.1,-0.3].
    assert_allclose(q,start+[.1,-.3],atol=1e-9); assert len(e)==2 and not ok
    q,ok,e=m.solve_planar_ik([1,1],start,[2,2],0,1e-12,.01); assert_array_equal(q,start); assert len(e)==1 and not ok
def invalid(m):
    for args in [([0,1],[0,0],[1,1],2,1e-6,.5),([1,1],[0,0],[1,1],True,1e-6,.5),([1,1],[0,0],[1,1],201,1e-6,.5),([1,1],[0,0],[1,1],2,0,.5),([1,1],[0,0],[1,1],2,1e-6,0)]:
        with np.testing.assert_raises(ValueError): m.solve_planar_ik(*args)
TESTS=[('Already converged','public',solved),('Unreachable singular target','public',unreachable),('Reachable nonlinear solve','hidden',reachable),('Independent one-step Jacobian oracle','hidden',exact_update),('Invalid IK settings','hidden',invalid)]

def tiny_denominator(m):
    with np.testing.assert_raises(ValueError): m.solve_planar_ik([1e-300,1],[0,0],[1,1],2,1e-6,.5)
TESTS.append(('Reject numerically unsupported denominator','hidden',tiny_denominator))
