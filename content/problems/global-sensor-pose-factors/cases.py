import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def args(n=1):return [np.tile(np.eye(4),(n,1,1)),np.eye(4),np.tile([1.,2.,3.],(n,1)),np.tile([1.,0.,0.],(n,1)),np.array([1.,0.,0.]),np.full(n,4.),np.ones((n,7)),np.ones((n,3),bool)]
def first(m):
    r=m.global_factors(*args());assert_allclose(r['raw'],[[1,2,3,0,0,0,4]]);assert r['cost']==15
def extrinsic(m):
    a=args();a[1][:3,:3]=[[0,-1,0],[1,0,0],[0,0,1]];a[1][0,3]=1;a[2][:]=[1,0,0];a[3][:]=[0,-2,0];a[4][:]=[5,0,0];a[5][:]=0;r=m.global_factors(*a);assert_allclose(r['raw'],np.zeros((1,7)));assert r['cost']==0
def oracle(m):
    rng=np.random.default_rng(851);a=args(2048);angles=rng.uniform(-3,3,2048);a[0][:,0,0]=a[0][:,1,1]=np.cos(angles);a[0][:,0,1]=-np.sin(angles);a[0][:,1,0]=np.sin(angles);a[0][:,:3,3]=rng.normal(size=(2048,3));a[1][:3,3]=[.2,-.4,.1];a[2]=rng.normal(size=(4096,3))[::2];a[3]=rng.normal(size=(2048,3));a[6]=rng.uniform(.1,2,(2048,7));a[7]=rng.random((2048,3))>.4;before=a[2].copy();r=m.global_factors(*a);expected=[]
    for i in range(2048):
        t=a[0][i]@a[1];parts=[a[2][i]-t[:3,3],a[3][i]/np.linalg.norm(a[3][i])-np.linalg.solve(t[:3,:3],a[4]/np.linalg.norm(a[4])),np.array([a[5][i]-t[2,3]])];expected.append(np.concatenate([p if a[7][i,j] else np.zeros(len(p)) for j,p in enumerate(parts)]))
    expected=np.array(expected);assert_allclose(r['raw'],expected,atol=1e-12);assert_allclose(r['whitened'],expected/a[6]);assert_allclose(r['cost'],.5*sum(float(x*x) for x in (expected/a[6]).flat));assert_array_equal(a[2],before);assert not np.shares_memory(r['raw'],a[2])
def empty(m):
    r=m.global_factors(*args(0));assert r['raw'].shape==(0,7) and r['cost']==0;a=args();a[-1][:]=False;assert m.global_factors(*a)['cost']==0
def invalid(m):
    for index,value in [(3,np.zeros((1,3))),(4,np.zeros(3)),(6,np.zeros((1,7))),(5,np.array([np.inf]))]:
        a=args();a[-1][:]=False;a[index]=value;bad(lambda:m.global_factors(*a))
TESTS=[('Three distinct sensor models','public',first),('Sensor lever arm and magnetic frame','public',extrinsic),('Scalar pose model oracle with missing sensors at scale','hidden',oracle),('Empty batch and unavailable evidence','hidden',empty),('Invalid masked data and undefined field direction','hidden',invalid)]
