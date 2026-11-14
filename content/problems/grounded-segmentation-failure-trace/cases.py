import numpy as np
from numpy.testing import assert_array_equal,assert_allclose
def example(m):
    r=m.grounded_segmentation(np.array([[.9,.2]]),np.array([[[True,True],[False,False]]]),np.array([.8]),.5,.5);assert r['status']==['accepted'];assert_array_equal(r['areas'],[2]);assert_array_equal(r['phrase_indices'],[0]);assert_allclose(r['centroids_xy'],[[1,.5]])
def failures(m):
    r=m.grounded_segmentation(np.array([[.2],[.9]]),np.zeros((2,2,2),bool),np.array([.1,.1]),.5,.5);assert r['status']==['low_grounding','low_mask_quality'];assert r['centroids_xy'].shape==(0,2)
def stages(m):
    masks=np.zeros((4,2,3),bool);masks[1,1,2]=True;masks[3,0,0]=True
    r=m.grounded_segmentation(np.array([[.5,.5]]*4),masks,np.array([.5,.5,.4,.6]),.5,.5)
    assert r['status']==['empty_mask','accepted','low_mask_quality','accepted'];assert_array_equal(r['query_indices'],[1,3]);assert_array_equal(r['phrase_indices'],[0,0]);assert_allclose(r['centroids_xy'],[[2.5,1.5],[.5,.5]])
def empty(m):
    r=m.grounded_segmentation(np.empty((0,2)),np.empty((0,2,3),bool),np.empty(0),0,0);assert r['status']==[] and r['centroids_xy'].shape==(0,2)
def invalid(m):
    for s,masks,q in [(np.array([[1.1]]),np.zeros((1,1,1),bool),np.ones(1)),(np.ones((1,1)),np.zeros((1,1,1)),np.ones(1)),(np.ones((1,1)),np.zeros((1,1,1),bool),np.ones(2))]:
        with np.testing.assert_raises(ValueError):m.grounded_segmentation(s,masks,q,.5,.5)
TESTS=[('Accepted geometry','public',example),('Failure precedence','public',failures),('Identity ties equality and empty masks','hidden',stages),('No queries','hidden',empty),('Validation','hidden',invalid)]

def scale_storage(m):
    masks=np.ones((128,128,256),bool)[:,:,::2];scores=np.ones((128,8))[:,::2];quality=np.ones(256)[::2];saved=masks.copy();r=m.grounded_segmentation(scores,masks,quality,.5,.5)
    assert r['status']==['accepted']*128;assert_array_equal(r['areas'],np.full(128,128*128));assert_allclose(r['centroids_xy'],np.full((128,2),64.));assert_array_equal(masks,saved)
    for out in (r['query_indices'],r['phrase_indices'],r['areas'],r['centroids_xy']):assert not np.shares_memory(out,masks)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
