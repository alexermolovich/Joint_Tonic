import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def example(m):
    uv,z=m.project_bev(np.array([[2.,4.,2.],[0.,0.,-1.]]),np.eye(4)[None],np.eye(3)[None]);assert_allclose(uv,[[[1,2],[0,0]]]);assert_allclose(z,[[2,-1]])
def cameras(m):
    t=np.repeat(np.eye(4)[None],2,axis=0);t[1,0,3]=1
    uv,z=m.project_bev(np.array([[0.,0.,2.]]),t,np.repeat(np.eye(3)[None],2,axis=0));assert_allclose(uv,[[[0,0]],[[.5,0]]]);assert_allclose(z,[[2],[2]])
def mechanism(m):
    r=np.random.default_rng(9);p=r.uniform(-3,3,(101,3));t=np.repeat(np.eye(4)[None],3,axis=0);t[:,2,3]=[1,3,5];k=np.repeat(np.eye(3)[None],3,axis=0);k[:,0,0]=[2,3,4];k[:,1,2]=7
    uv,z=m.project_bev(p,t,k)
    for c in range(3):
        for n in range(len(p)):
            q=t[c,:3,:3]@p[n]+t[c,:3,3];assert_allclose(z[c,n],q[2]);expected=[k[c,0,0]*q[0]/q[2],q[1]/q[2]+7] if q[2]>1e-6 else [0,0];assert_allclose(uv[c,n],expected)
def boundary(m):
    uv,z=m.project_bev(np.array([[1.,2.,1e-6],[1.,2.,2e-6]]),np.eye(4)[None],np.eye(3)[None]);assert_allclose(uv[0,0],0);assert_allclose(uv[0,1],[5e5,1e6])
    uv,z=m.project_bev(np.empty((0,3)),np.eye(4)[None],np.eye(3)[None]);assert uv.shape==(1,0,2) and z.shape==(1,0)
def rotated(m):
    # Proper +90 degree rotation around optical y: ego +x points behind camera.
    t=np.eye(4)[None];t[0,:3,:3]=[[0,0,1],[0,1,0],[-1,0,0]]
    uv,z=m.project_bev(np.array([[-2.,4.,6.],[2.,0.,1.]]),t,np.eye(3)[None])
    assert_allclose(z,[[2,-2]]);assert_allclose(uv,[[[3,2],[0,0]]])
def invalid(m):
    for p,t,k in [(np.ones((1,2)),np.eye(4)[None],np.eye(3)[None]),(np.ones((1,3)),(np.eye(4)*2)[None],np.eye(3)[None]),(np.ones((1,3)),np.eye(4)[None],np.zeros((1,3,3)))]:
        with np.testing.assert_raises(ValueError):m.project_bev(p,t,k)
def storage(m):
    p=np.arange(18.).reshape(3,6)[:,::2];t=np.eye(4)[None];k=np.eye(3)[None];copies=[x.copy() for x in (p,t,k)];uv,z=m.project_bev(p,t,k)
    for x,c in zip((p,t,k),copies):assert_array_equal(x,c);assert not np.shares_memory(x,uv);assert not np.shares_memory(x,z)
TESTS=[('Signed depth','public',example),('Two cameras','public',cameras),('Scalar camera oracle','hidden',mechanism),('Nonidentity rotation direction','hidden',rotated),('Depth cutoff and empty points','hidden',boundary),('Validation','hidden',invalid),('Storage','hidden',storage)]
