import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def args():return [np.tile(np.eye(3),(2,1,1)),np.zeros((2,3)),np.zeros((2,3)),np.zeros(3),1.,np.eye(3),np.zeros(3),np.zeros(3),np.ones(9),np.empty((0,2)),np.empty((0,2))]
def stationary(m):
 a=args();a[3]=np.array([0.,0.,-10.]);a[4]=.1;a[6]=np.array([0.,0.,1.]);a[7]=np.array([0.,0.,.05]);r=m.keyframe_residual(*a);assert_allclose(r['inertial'],0,atol=1e-15);assert r['cost']<1e-25
def combined(m):
 a=args();a[1][1,0]=1;a[9]=np.array([[3.,4.]]);a[10]=np.ones((1,2));r=m.keyframe_residual(*a);assert_array_equal(r['inertial'],[0,0,0,0,0,0,1,0,0]);assert r['cost']==13
def oracle(m):
 rng=np.random.default_rng(844);a=args();theta=.7;r0=np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1.]]);phi=.2;error=np.array([[1.,0,0],[0,np.cos(phi),-np.sin(phi)],[0,np.sin(phi),np.cos(phi)]]);dr=np.array([[0.,-1,0],[1,0,0],[0,0,1.]]);a[0]=np.stack([r0,r0@dr@error]);a[5]=dr;a[1]=rng.normal(size=(2,3));a[2]=rng.normal(size=(2,3));a[3]=np.array([0.,0.,-9.81]);a[4]=.2;a[6]=rng.normal(size=3);a[7]=rng.normal(size=3);a[8]=np.arange(1,10,dtype=float);a[9]=rng.normal(size=(4096,4))[:,::2];a[10]=rng.uniform(.5,2,(4096,2));before=a[9].copy();r=m.keyframe_residual(*a)
 # Coordinate-wise sums independently verify frame mapping and uncertainty order.
 velocity=np.array([sum(r0[j,k]*(a[2][1,j]-a[2][0,j]-a[3][j]*.2) for j in range(3))-a[6][k] for k in range(3)]);position=np.array([sum(r0[j,k]*(a[1][1,j]-a[1][0,j]-a[2][0,j]*.2-a[3][j]*.02) for j in range(3))-a[7][k] for k in range(3)]);expected=np.r_[[phi,0,0],velocity,position];white=np.r_[expected/a[8],(a[9]/a[10]).ravel()];assert_allclose(r['inertial'],expected,atol=1e-12);assert_allclose(r['whitened'],white,atol=1e-12);assert_allclose(r['cost'],sum(float(x)**2 for x in white)/2);assert_array_equal(a[9],before);assert not np.shares_memory(r['whitened'],a[9])
def edges(m):
 for angle in [1e-12,np.pi-1.001e-4]:
  a=args();a[0][1]=np.array([[np.cos(angle),-np.sin(angle),0],[np.sin(angle),np.cos(angle),0],[0,0,1.]]);r=m.keyframe_residual(*a);assert_allclose(r['inertial'][:3],[0,0,angle],atol=1e-12)
def invalid(m):
 a=args();a[4]=10**1000;bad(lambda:m.keyframe_residual(*a));a=args();a[8][0]=0;bad(lambda:m.keyframe_residual(*a));a=args();a[0][1]=np.diag([-1.,-1.,1.]);bad(lambda:m.keyframe_residual(*a));a=args();a[5]=np.ones((3,3));bad(lambda:m.keyframe_residual(*a))
TESTS=[('Stationary gravity cancellation','public',stationary),('Combined whitened visual and inertial cost','public',combined),('Independent rotated frame and scalar whitening oracle at scale','hidden',oracle),('Small and near-principal-branch angles','hidden',edges),('Invalid rotations uncertainties and duration','hidden',invalid)]
