import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def one(m):
    z=m.encode_points(np.zeros((2,2)),np.array([0,1],dtype=np.int64),(1,1),np.array([[1.],[0.]]),np.array([[0.,0],[2,3]]));assert_allclose(z,[[0,1],[2,4]],atol=1e-12)
def phase(m):assert_allclose(m.encode_points(np.zeros((1,2)),np.zeros(1,dtype=np.int64),(2,2),np.array([[.5],[0.]]),np.zeros((2,2))),[[-1,0]],atol=1e-12)
def oracle(m):
    p=np.array([[0.,0],[3,1],[1,1]]);l=np.array([1,0,1],dtype=np.int64);f=np.array([[.1,.3],[-.2,.7]]);e=np.arange(8.).reshape(2,4);old=p.copy();z=m.encode_points(p,l,(2,4),f,e)
    expected=[]
    for i,(x,y) in enumerate(p):
        q=[2*(x+.5)/4-1,2*(y+.5)/2-1];a=[2*np.pi*sum(q[k]*f[k,j] for k in range(2)) for j in range(2)];expected.append(np.r_[np.sin(a),np.cos(a)]+e[l[i]])
    assert_allclose(z,expected);assert_array_equal(p,old)
def empty(m):assert m.encode_points(np.empty((0,2)),np.empty(0,dtype=np.int64),(2,4),np.ones((2,3)),np.zeros((2,6))).shape==(0,6)
def invalid(m):
    for p,l,size,f,e in [(np.array([[2.,0]]),np.array([0],dtype=np.int64),(2,2),np.ones((2,1)),np.zeros((2,2))),(np.zeros((1,2)),np.array([-1],dtype=np.int64),(2,2),np.ones((2,1)),np.zeros((2,2))),(np.zeros((1,2)),np.array([0],dtype=np.int64),[2,2],np.ones((2,1)),np.zeros((2,2)))]:
        with np.testing.assert_raises(ValueError):m.encode_points(p,l,size,f,e)
TESTS=[('Type semantics','public',one),('Centered Fourier phase','public',phase),('Nonsquare scalar oracle','hidden',oracle),('No prompts','hidden',empty),('Validation','hidden',invalid)]

def scale_storage(m):
    rng=np.random.default_rng(91);points=rng.uniform(0,1,(1024,4))[:,::2]*np.array([99,49]);labels=np.arange(2048,dtype=np.int64)[::2]%2;f=rng.uniform(-1,1,(2,64));e=rng.normal(size=(2,128));saved=[a.copy() for a in (points,labels,f,e)];out=m.encode_points(points,labels,(50,100),f,e)
    assert out.shape==(1024,128) and out.dtype==np.float64
    for a,b in zip((points,labels,f,e),saved):assert_array_equal(a,b);assert not np.shares_memory(a,out)
    expected=m.encode_points(points[:1].copy(),labels[:1].copy(),(50,100),f,e);assert_allclose(out[:1],expected,atol=1e-10)

TESTS.append(('Scale noncontiguous and noalias','hidden',scale_storage))
