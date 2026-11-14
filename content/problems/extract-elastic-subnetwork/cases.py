"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def center(m):
 out=m.extract_subnetwork([np.arange(9,dtype=np.float64).reshape(1,1,3,3)],1,1,1);assert len(out)==1;np.testing.assert_array_equal(out[0],[[[[4.]]]])
def shrink(m):
 out=m.extract_subnetwork([np.full((2,2,3,3),2.),np.full((2,2,3,3),3.)],1,1,3);assert len(out)==1;np.testing.assert_array_equal(out[0],np.full((1,1,3,3),2.))
def storage(m):
 a=(np.arange(4*4*5*5,dtype=np.float64)%101).reshape(4,4,5,5)[:,:,::-1,::-1];before=a.copy();out=m.extract_subnetwork([a,a],2,2,3)
 expected=np.array([[[[a[o,i,y+1,x+1] for x in range(3)] for y in range(3)] for i in range(2)] for o in range(2)])
 for x in out:assert x.dtype==np.float64 and not np.shares_memory(x,a);np.testing.assert_array_equal(x,expected)
 assert not np.shares_memory(out[0],out[1]);out[0][:]=0;np.testing.assert_array_equal(a,before);np.testing.assert_array_equal(out[1],expected)
def scale(m):
 weights=[np.ones((32,32,7,7)) for _ in range(16)];out=m.extract_subnetwork(weights,16,16,5);assert len(out)==16
 for layer in out:assert layer.shape==(16,16,5,5) and np.all(layer==1)
def invalid(m):
 a=np.ones((2,2,3,3))
 for weights,d,w,k in [([],1,1,1),([a.astype(np.float32)],1,1,1),([a],True,1,1),([a],1,3,1),([a],1,1,2),([a,np.full_like(a,np.nan)],1,1,1),([a,np.zeros((1,1,3,3))],1,1,1),([np.zeros((2,1,3,3))],1,1,1),([np.zeros((2,2,2,2))],1,1,1),([np.full_like(a,101.)],1,1,1),([np.ones((64,64,9,9))]*4,1,1,1)]:rejects(lambda:m.extract_subnetwork(weights,d,w,k))

TESTS=[('Centered crop', 'public', center), ('Depth and width selection', 'public', shrink), ('Independent scalar crop noncontiguous aliases', 'hidden', storage), ('Sixteen-layer bounded stack', 'hidden', scale), ('Validate every layer and parameter', 'hidden', invalid)]
