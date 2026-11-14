import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def first(m):
 c=np.eye(4)[None].copy();c[0,0,3]=1;assert_array_equal(m.deskew_points(np.array([[2.,0,0]]),c,np.eye(4)),[[3,0,0]])
def second(m):
 c=np.eye(4)[None].copy();c[0,0,3]=1;r=np.eye(4);r[0,3]=2;assert_array_equal(m.deskew_points(np.array([[2.,0,0]]),c,r),[[1,0,0]])
def oracle(m):
 n=8192;rng=np.random.default_rng(825);p=rng.normal(size=(n,6))[:,::2];c=np.tile(np.eye(4),(n,1,1));angles=np.linspace(-1,1,n)
 for i,a in enumerate(angles):c[i,:3,:3]=rz(a)
 c[:,:3,3]=rng.normal(size=(n,3));ref=np.eye(4);ref[:3,:3]=np.array([[1.,0,0],[0,0,-1],[0,1,0]]);ref[:3,3]=[2.,1,-.5];before=[p.copy(),c.copy(),ref.copy()];out=m.deskew_points(p,c,ref);inv=np.linalg.inv(ref)
 expected=np.array([(inv@c[i]@np.r_[p[i],1])[:3] for i in range(0,n,47)]);assert_allclose(out[::47],expected,atol=1e-12)
 for a,b in zip(before,[p,c,ref]):assert_array_equal(a,b)
 assert not np.shares_memory(out,p)
def identity(m):
 ref=np.eye(4);ref[:3,:3]=rz(.7);ref[:3,3]=[1,2,3];p=np.array([[1.,2,3]]);assert_allclose(m.deskew_points(p,ref[None],ref),p,atol=1e-12)
 assert m.deskew_points(np.empty((0,3)),np.empty((0,4,4)),np.eye(4)).shape==(0,3)
def invalid(m):
 for p,c,r in [(np.ones((1,2)),np.eye(4)[None],np.eye(4)),(np.ones((1,3)),np.zeros((1,4,4)),np.eye(4)),(np.ones((1,3)),np.eye(4)[None],np.zeros((4,4)))]:bad(lambda:m.deskew_points(p,c,r))
TESTS=[('Capture-to-world motion','public',first),('Reference-frame inverse','public',second),('Independent homogeneous oracle at scan scale','hidden',oracle),('Identical poses and empty scan','hidden',identity),('Invalid capture poses','hidden',invalid)]
