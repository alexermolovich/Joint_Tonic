import numpy as np
from numpy.testing import assert_allclose
def call(m,z,p,l,t,i,e=.1):return m.detr_losses(np.array(z,dtype=float),np.array(p,dtype=float).reshape(-1,4),np.array(l,dtype=np.int64),np.array(t,dtype=float).reshape(-1,4),np.array(i,dtype=np.int64),e)
def identical(m):
    b=[.5,.5,1,1];r=call(m,[[0,0]],[b],[0],[b],[0]);assert_allclose(r['classification'],np.log(2));assert r['l1']==r['giou']==0
def touching(m):
    r=call(m,[[0,0]],[[.25,.5,.5,1]],[0],[[.75,.5,.5,1]],[0]);assert_allclose([r['l1'],r['giou'],r['total']],[.5,1,np.log(2)+4.5])
def weighted(m):
    b=[.5,.5,1,1];r=call(m,[[np.log(3),0],[np.log(3),0]],[b,b],[0],[b],[1],.25);expected=(.25*np.log(4)+np.log(4/3))/1.25;assert_allclose(r['classification'],expected)
    empty=call(m,[[1000,0]],[b],[],[],[],.2);assert_allclose(empty['classification'],1000);assert empty['l1']==empty['giou']==0
def giou(m):
    r=call(m,[[0,0]],[[.1,.5,.2,.2]],[0],[[.9,.5,.2,.2]],[0]);assert_allclose(r['l1'],.8);assert_allclose(r['giou'],1.6)
    # Coordinates beyond the image are not clipped: same-size boxes displaced by half their width.
    r=call(m,[[0,0]],[[0.,.5,1,1]],[0],[[.5,.5,1,1]],[0]);assert_allclose(r['giou'],2/3)
def invalid(m):
    b=[.5,.5,1,1]
    for z,p,l,t,i in [([[0,0]],[b],[1],[b],[0]),([[0,0],[0,0]],[b,b],[0,0],[b,b],[0,0]),([[0,0]],[b],[0],[b],[1]),([[0,0]],[[.5,.5,0,1]],[0],[b],[0])]:
        with np.testing.assert_raises(ValueError):call(m,z,p,l,t,i)
TESTS=[('Identical matched box','public',identical),('Touching boxes','public',touching),('Weighted background reduction and stable logits','hidden',weighted),('Negative GIoU and unclipped corners','hidden',giou),('Validation','hidden',invalid)]

def scale_storage(m):
    q=256;c=64;z=np.zeros((q,2*(c+1)))[:,::2];p=np.ones((q,8))[:,::2]*.5;t=p[::2].copy();idx=np.arange(0,q,2,dtype=np.int64);labels=np.arange(len(t),dtype=np.int64)%c;saved=p.copy();r=m.detr_losses(z,p,labels,t,idx,.1)
    assert_allclose(r['classification'],np.log(c+1));assert_allclose(r['l1'],0);assert_allclose(r['giou'],0);assert_allclose(p,saved)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
