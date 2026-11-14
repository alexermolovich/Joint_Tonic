import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
    poses=np.tile(np.eye(4),(2,1,1));poses[1,0,3]=2;z=np.eye(4);z[0,3]=1;r=m.imu_lidar_residual(poses,np.eye(4),z,np.ones(6));assert_allclose(r['translation'],[1,0,0]);assert_allclose(r['rotation'],0);assert r['cost']==.5
def lever(m):
    poses=np.tile(np.eye(4),(2,1,1));poses[1,:3,:3]=[[0,-1,0],[1,0,0],[0,0,1]];ext=np.eye(4);ext[0,3]=1;z=np.eye(4);z[:3,:3]=poses[1,:3,:3];z[:3,3]=[-1,1,0];r=m.imu_lidar_residual(poses,ext,z,np.ones(6));assert_allclose(r['predicted'],z);assert_allclose(r['cost'],0,atol=1e-15)
def axis(v):
    angle=np.linalg.norm(v)
    if angle==0:return np.eye(3)
    u=v/angle;x,y,z=u;k=np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]]);return np.cos(angle)*np.eye(3)+(1-np.cos(angle))*np.outer(u,u)+np.sin(angle)*k
def oracle(m):
    rng=np.random.default_rng(854)
    for k in range(128):
        p=np.tile(np.eye(4),(4,1,1))[::2];ext=np.eye(4);z=np.eye(4)
        for t in [p[0],p[1],ext]:t[:3,:3]=axis(rng.normal(size=3));t[:3,3]=rng.normal(size=3)
        pred=np.linalg.solve(p[0]@ext,p[1]@ext);v=rng.normal(size=3);v*=rng.uniform(1e-5,2.8)/np.linalg.norm(v);err=np.eye(4);err[:3,:3]=axis(v);err[:3,3]=rng.normal(size=3);z=pred@np.linalg.inv(err);std=rng.uniform(.1,2,6);before=p.copy();r=m.imu_lidar_residual(p,ext,z,std);expected=np.r_[err[:3,3],v]/std;assert_allclose(r['predicted'],pred,atol=1e-10);assert_allclose(r['rotation'],v,atol=1e-10);assert_allclose(r['whitened'],expected,atol=1e-10);assert_allclose(r['cost'],.5*sum(expected**2));assert_array_equal(p,before);assert not np.shares_memory(p,r['predicted'])
def branch(m):
    for theta in [1e-9,np.pi-2e-4]:
        p=np.tile(np.eye(4),(2,1,1));p[1,:3,:3]=axis(np.array([theta,0.,0.]));r=m.imu_lidar_residual(p,np.eye(4),np.eye(4),np.ones(6));assert_allclose(r['rotation'],[theta,0,0],atol=1e-9)
def invalid(m):
    p=np.tile(np.eye(4),(2,1,1));bad(lambda:m.imu_lidar_residual(p,np.eye(4),np.eye(4),np.zeros(6)));p[1,:3,:3]=np.diag([1.,-1,-1]);bad(lambda:m.imu_lidar_residual(p,np.eye(4),np.eye(4),np.ones(6)));p[1,:3,:3]=np.diag([-1.,1,1]);bad(lambda:m.imu_lidar_residual(p,np.eye(4),np.eye(4),np.ones(6)))
TESTS=[('Translation mismatch','public',first),('Rotation-induced lidar lever arm','public',lever),('Constructed noncommuting residual oracle and strided storage','hidden',oracle),('Small and near-pi principal rotation errors','hidden',branch),('Invalid noise reflection and excluded log branch','hidden',invalid)]
