import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def fixtures():
    A=np.tile(np.eye(4),(2,1,1)); A[0,:3,:3]=np.diag([1,-1,-1]); A[1,:3,:3]=np.diag([-1,1,-1]); return A
def example(m):
    A=fixtures(); B=A.copy(); B[:,:3,3]=[[0,-4,-6],[-2,0,-6]]; t,e=m.solve_hand_eye_translation(A,B,np.eye(3)); assert_allclose(t,[1,2,3]); assert_allclose(e,0,atol=1e-9)
def zero(m):
    A=fixtures(); t,e=m.solve_hand_eye_translation(A,A,np.eye(3)); assert_allclose(t,0,atol=1e-9); assert_allclose(e,0,atol=1e-9)
def generated_mount(m):
    A=fixtures(); A[:,:3,3]=[[.2,1,-1],[2,.3,1]]; X=np.eye(4); X[:3,:3]=[[0,-1,0],[1,0,0],[0,0,1]]; X[:3,3]=[.3,-.4,1.2]
    B=np.array([np.linalg.inv(X)@a@X for a in A]); old=A.copy(); t,e=m.solve_hand_eye_translation(A,B,X[:3,:3]); assert_allclose(t,X[:3,3],atol=1e-9); assert_allclose(e,0,atol=1e-9); assert_array_equal(A,old)
def noisy_optimum(m):
    A=fixtures(); B=A.copy(); B[:,:3,3]=[[.2,1,2],[3,4,5]]; t,e=m.solve_hand_eye_translation(A,B,np.eye(3)); C=(A[:,:3,:3]-np.eye(3)).reshape(-1,3)
    assert_allclose(C.T@e.reshape(-1),0,atol=1e-9); assert np.linalg.norm(e)>0
def invalid(m):
    A=fixtures(); repeated=np.stack([A[0],A[0]])
    with np.testing.assert_raises(ValueError): m.solve_hand_eye_translation(repeated,repeated,np.eye(3))
    bad=A.copy(); bad[0,3,0]=1
    with np.testing.assert_raises(ValueError): m.solve_hand_eye_translation(bad,A,np.eye(3))
    with np.testing.assert_raises(ValueError): m.solve_hand_eye_translation(A,A,np.diag([1,1,-1]))
TESTS=[('Observable translation','public',example),('Zero mounting offset','public',zero),('Independent AX=XB construction','hidden',generated_mount),('Noisy least-squares normal equation','hidden',noisy_optimum),('Unobservable or malformed motions','hidden',invalid)]
