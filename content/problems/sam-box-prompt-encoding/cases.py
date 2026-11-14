import numpy as np
from numpy.testing import assert_allclose
def one(m):assert_allclose(m.encode_boxes(np.zeros((1,4)),(1,1),np.array([[1.],[0.]]),np.array([[1.,2],[3,4]])),[[[1,3],[3,5]]],atol=1e-12)
def phase(m):assert_allclose(m.encode_boxes(np.array([[0.,0,1,1]]),(2,2),np.array([[.5],[0.]]),np.zeros((2,2))),[[[-1,0],[1,0]]],atol=1e-12)
def oracle(m):
    b=np.array([[0.,1,3,1],[1,0,2,1]]);f=np.array([[.3,.8],[.2,-.1]]);e=np.arange(8.).reshape(2,4);z=m.encode_boxes(b,(2,4),f,e)
    for i,box in enumerate(b):
        for k in range(2):
            p=box[k*2:k*2+2];q=2*(p+.5)/[4,2]-1;a=2*np.pi*(q[0]*f[0]+q[1]*f[1]);assert_allclose(z[i,k],np.r_[np.sin(a),np.cos(a)]+e[k])
    assert m.encode_boxes(np.empty((0,4)),(2,4),f,e).shape==(0,2,4)
def invalid(m):
    for b,size in [(np.array([[1.,0,0,1]]),(2,2)),(np.array([[0.,0,2,1]]),(2,2)),(np.zeros((1,4)),(True,2)),(np.zeros((1,3)),(2,2))]:
        with np.testing.assert_raises(ValueError):m.encode_boxes(b,size,np.ones((2,1)),np.zeros((2,2)))
TESTS=[('Corner identity','public',one),('Spatial corners','public',phase),('Nonsquare corner oracle and empty','hidden',oracle),('Validation','hidden',invalid)]

def scale_storage(m):
    base=np.tile(np.array([0.,0.,99.,49.,0.,0.,99.,49.]),(1024,1));boxes=base[:,::2].copy();boxes[:]=[0,0,99,49];boxes=np.repeat(boxes,2,axis=1)[:,::2];f=np.arange(64.).reshape(2,32)/100;e=np.zeros((2,64));saved=boxes.copy();out=m.encode_boxes(boxes,(50,100),f,e)
    assert out.shape==(1024,2,64) and out.dtype==np.float64;assert_allclose(boxes,saved)
    for a in (boxes,f,e):assert not np.shares_memory(a,out)
    assert_allclose(out[0],out[-1])

TESTS.append(('Scale noncontiguous and noalias','hidden',scale_storage))
