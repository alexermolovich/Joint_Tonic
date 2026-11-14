import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def example(m):
    r=m.assign_yolo_cells(np.array([[.75,.25,.2,.4]]),np.array([2],dtype=np.int64),2,3);assert r['object_indices'][0,1]==0 and r['class_ids'][0,1]==2;assert_allclose(r['box_targets'][0,1],[.5,.5,.2,.4]);assert (r['object_indices']==-1).sum()==3
def collision(m):
    r=m.assign_yolo_cells(np.array([[.1,.1,.2,.2],[.2,.2,.4,.4]]),np.array([0,1],dtype=np.int64),2,2);assert r['object_indices'][0,0]==1
def boundaries(m):
    r=m.assign_yolo_cells(np.array([[0.,0,.5,.5],[.5,.5,.5,.5],[.6,.6,.5,.5]]),np.array([0,1,0],dtype=np.int64),2,2);assert_array_equal(r['object_indices'],[[0,-1],[-1,1]]);assert_allclose(r['box_targets'][1,1,:2],[0,0])
    r=m.assign_yolo_cells(np.empty((0,4)),np.empty(0,dtype=np.int64),3,2);assert (r['class_ids']==-1).all();assert not r['box_targets'].any()
def oracle(m):
    rng=np.random.default_rng(17);b=np.column_stack([rng.uniform(0,1,(300,2)),rng.uniform(.01,1,(300,2))]);labels=rng.integers(0,3,300,dtype=np.int64);out=m.assign_yolo_cells(b,labels,8,3)
    for r in range(8):
        for c in range(8):
            ids=[i for i,row in enumerate(b) if int(row[1]*8)==r and int(row[0]*8)==c];expected=min(ids,key=lambda i:(-b[i,2]*b[i,3],i)) if ids else -1;assert out['object_indices'][r,c]==expected
def invalid(m):
    for b,l,s,c in [(np.array([[1.,0,.2,.2]]),np.array([0],dtype=np.int64),2,2),(np.array([[0.,0,0,.2]]),np.array([0],dtype=np.int64),2,2),(np.array([[0.,0,.2,.2]]),np.array([2],dtype=np.int64),2,2),(np.empty((0,4)),np.empty(0,dtype=np.int64),True,2)]:
        with np.testing.assert_raises(ValueError):m.assign_yolo_cells(b,l,s,c)
TESTS=[('Cell-relative target','public',example),('Crowded cell policy','public',collision),('Grid boundaries ties and empty input','hidden',boundaries),('Independent cell enumeration','hidden',oracle),('Validation','hidden',invalid)]

def scale_storage(m):
    rows,cols=np.indices((64,64));b=np.column_stack(((cols.ravel()+.5)/64,(rows.ravel()+.5)/64,np.full(4096,.01),np.full(4096,.01)));b=np.repeat(b,2,axis=1)[:,::2];labels=np.arange(8192,dtype=np.int64)[::2]%3;saved=b.copy();r=m.assign_yolo_cells(b,labels,64,3)
    assert_array_equal(r['object_indices'],np.arange(4096).reshape(64,64));assert_allclose(r['box_targets'][...,:2],.5);assert_array_equal(r['class_ids'],labels.reshape(64,64));assert_array_equal(b,saved)
    for out in r.values():assert not np.shares_memory(out,b)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
