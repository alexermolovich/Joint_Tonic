import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def example(m):
    r=m.decode_grounded_boxes(np.array([[.5,.5,.5,1.]]),np.zeros((1,2)),np.eye(2,dtype=bool),(100,200),.5);assert_array_equal(r['query_indices'],[0]);assert_array_equal(r['phrase_indices'],[0]);assert_allclose(r['scores'],[.5]);assert_allclose(r['boxes_xyxy'],[[50,0,150,100]])
def unclipped(m):assert_allclose(m.decode_grounded_boxes(np.array([[0.,0,1,1]]),np.zeros((1,1)),np.ones((1,1),bool),(10,20),.5)['boxes_xyxy'],[[-10,-5,10,5]])
def logits(m):
    b=np.repeat(np.array([[.5,.5,.2,.4]]),3,axis=0);s=np.array([[-1000.,-1000,1000],[0,0,0],[-10,-20,-30]]);p=np.array([[True,True,False],[False,False,True]])
    r=m.decode_grounded_boxes(b,s,p,(20,40),.5);assert_array_equal(r['query_indices'],[0,1]);assert_array_equal(r['phrase_indices'],[1,0]);assert_allclose(r['scores'],[1,.5]);assert np.isfinite(r['boxes_xyxy']).all()
def empty(m):
    r=m.decode_grounded_boxes(np.empty((0,4)),np.empty((0,2)),np.ones((1,2),bool),(2,3),1);assert r['boxes_xyxy'].shape==(0,4);assert r['query_indices'].dtype==r['phrase_indices'].dtype==np.int64
def invalid(m):
    for b,s,p in [(np.array([[.5,.5,0.,1.]]),np.zeros((1,1)),np.ones((1,1),bool)),(np.array([[.5,.5,1.,1.]]),np.zeros((1,1)),np.zeros((1,1),bool)),(np.array([[.5,.5,1.,1.]]),np.zeros((2,1)),np.ones((1,1),bool))]:
        with np.testing.assert_raises(ValueError):m.decode_grounded_boxes(b,s,p,(2,3),.5)
TESTS=[('Tie and pixel conversion','public',example),('Unclipped corners','public',unclipped),('Stable logits and query order','hidden',logits),('No queries','hidden',empty),('Validation','hidden',invalid)]

def scale_storage(m):
    base=np.tile([.5,.5,.2,.4,.5,.5,.2,.4],(1024,1));boxes=base[:,::2].copy();boxes[:]=[.5,.5,.2,.4];boxes=np.repeat(boxes,2,axis=1)[:,::2];scores=np.zeros((1024,16))[:,::2];phrases=np.eye(8,dtype=bool);saved=boxes.copy();r=m.decode_grounded_boxes(boxes,scores,phrases,(100,200),.5)
    assert_array_equal(r['query_indices'],np.arange(1024));assert_array_equal(r['phrase_indices'],np.zeros(1024,dtype=np.int64));assert_allclose(r['scores'],.5);assert_allclose(r['boxes_xyxy'],np.tile([80,30,120,70],(1024,1)));assert_array_equal(boxes,saved)
    for out in r.values():
        for a in (boxes,scores,phrases):assert not np.shares_memory(out,a)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
