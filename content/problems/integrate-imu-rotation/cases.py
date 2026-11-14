import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def first(m):
 r=m.integrate_imu_rotation(np.array([[0.,0,np.pi/2]]),np.zeros(3),np.ones(1));assert_allclose(r['rotations'],np.stack([np.eye(3),rz(np.pi/2)]),atol=1e-12);assert_array_equal(r['elapsed'],[0,1])
def bias(m):
 b=np.array([1.,2,3]);r=m.integrate_imu_rotation(np.tile(b,(3,1)),b,np.array([.1,.2,.3]));assert_array_equal(r['rotations'],np.tile(np.eye(3),(4,1,1)))
def noncommuting(m):
 rx=np.array([[1.,0,0],[0,np.cos(.3),-np.sin(.3)],[0,np.sin(.3),np.cos(.3)]]);ry=np.array([[np.cos(.4),0,np.sin(.4)],[0,1,0],[-np.sin(.4),0,np.cos(.4)]]);r=m.integrate_imu_rotation(np.array([[.3,0,0],[0,.4,0]]),np.zeros(3),np.ones(2));assert_allclose(r['rotations'][-1],rx@ry,atol=1e-12);assert not np.allclose(r['rotations'][-1],ry@rx)
def scale(m):
 n=4096;w=np.zeros((n,6))[:,::2];w[:,2]=.25;b=np.array([0.,0,.05]);dt=np.full(n,1/128);before=w.copy();r=m.integrate_imu_rotation(w,b,dt)
 for k in range(0,n+1,67):assert_allclose(r['rotations'][k],rz(k*.2/128),atol=1e-11)
 assert_allclose(r['rotations'].transpose(0,2,1)@r['rotations'],np.tile(np.eye(3),(n+1,1,1)),atol=1e-11);assert_array_equal(w,before);assert not np.shares_memory(r['rotations'],w)
 r=m.integrate_imu_rotation(np.empty((0,3)),np.zeros(3),np.empty(0));assert_array_equal(r['rotations'],np.eye(3)[None]);assert_array_equal(r['elapsed'],[0])
def invalid(m):
 for w,b,dt in [(np.zeros((1,3)),np.zeros(3),np.zeros(1)),(np.ones((1,3))*101,np.zeros(3),np.ones(1)),(np.zeros((101,3)),np.zeros(3),np.ones(101)),(np.zeros((1,2)),np.zeros(3),np.ones(1))]:bad(lambda:m.integrate_imu_rotation(w,b,dt))
TESTS=[('One body rotation','public',first),('Bias cancellation','public',bias),('Noncommuting right composition','hidden',noncommuting),('Long scan scale, orthogonality and empty input','hidden',scale),('Invalid IMU intervals','hidden',invalid)]
