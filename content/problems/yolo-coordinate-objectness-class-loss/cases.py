import numpy as np
from numpy.testing import assert_allclose
def fixture():
    p=np.array([[[[.5,.5,.25,1],[.5,.5,1,1]]]]);c=np.array([[[.5,.2]]]);a=np.array([[[.8,.2]]]);t=np.array([[[.5,.5,1,1]]]);l=np.array([[0]],dtype=np.int64);r=np.array([[0]],dtype=np.int64);iou=np.ones((1,1));return p,c,a,t,l,r,iou
def perfect(m):
    p=np.array([[[[.5,.5,1.,1.]]]]);r=m.yolo_loss(p,np.ones((1,1,1)),np.ones((1,1,1)),p[:,:,0].copy(),np.zeros((1,1),dtype=np.int64),np.zeros((1,1),dtype=np.int64),np.ones((1,1)));assert all(v==0 for v in r.values())
def example(m):
    r=m.yolo_loss(*fixture());assert_allclose([r[k] for k in ('coordinate','objectness','classification','total')],[1.25,.27,.08,1.6])
def empty(m):
    args=list(fixture());args[4][:]=-1;args[5][:]=-1;r=m.yolo_loss(*args);assert_allclose(r['total'],.5*(.25+.04));assert r['coordinate']==r['classification']==0
def iou_target(m):
    args=list(fixture());args[-1][:]=.5;r=m.yolo_loss(*args);assert_allclose(r['objectness'],.02)
    args[5][:]=1;r=m.yolo_loss(*args);assert_allclose(r['coordinate'],0);assert_allclose(r['objectness'],.09+.125)
def invalid(m):
    for pos,val in [(4,np.array([[2]],dtype=np.int64)),(5,np.array([[-1]],dtype=np.int64)),(2,np.array([[[.8,.3]]])),(0,np.zeros((1,1,2,4)))]:
        a=list(fixture());a[pos]=val
        with np.testing.assert_raises(ValueError):m.yolo_loss(*a)
TESTS=[('Perfect prediction','public',perfect),('Three loss routes','public',example),('Empty cell background only','hidden',empty),('IoU target and predictor responsibility','hidden',iou_target),('Validation','hidden',invalid)]

def scale_storage(m):
    s=16;b=8;c=64;p=np.ones((s,s,b,8))[:,:,:,::2]*.5;t=np.ones((s,s,8))[:,:,::2]*.5;confidence=np.ones((s,s,b))*.2;a=np.ones((s,s,c))/c;labels=np.zeros((s,s),dtype=np.int64);responsible=np.zeros((s,s),dtype=np.int64);iou=np.ones((s,s))*.6;saved=p.copy();r=m.yolo_loss(p,confidence,a,t,labels,responsible,iou)
    assert_allclose(r['coordinate'],0);assert_allclose(r['objectness'],s*s*((.2-.6)**2+.5*(b-1)*.2**2));assert_allclose(r['classification'],s*s*(1-1/c));assert_allclose(p,saved)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
