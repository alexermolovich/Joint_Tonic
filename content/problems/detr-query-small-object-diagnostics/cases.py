import numpy as np
from numpy.testing import assert_array_equal
def example(m):
    r=m.diagnose_queries(np.array([[1.,0],[2,0]]),np.array([[0.,0,.1,.1]]*2),np.array([[0.,0,.1,.1],[.8,.8,.9,.9]]),.99,.5,.02);assert_array_equal(r['similar_pairs'],[[0,1]]);assert_array_equal(r['missed_small_indices'],[1])
def empty(m):
    r=m.diagnose_queries(np.empty((0,2)),np.empty((0,4)),np.array([[0.,0,.1,.1],[0,0,1,1]]),.9,.5,.02);assert r['similar_pairs'].shape==(0,2);assert_array_equal(r['missed_small_indices'],[0])
def boundaries(m):
    f=np.array([[1.,0],[0,1],[-1,0]]);p=np.array([[0.,0,.5,.5]]*3);r=m.diagnose_queries(f,p,np.array([[0.,0,.5,.5]]),0,1,.25);assert_array_equal(r['similar_pairs'],[[0,1],[1,2]]);assert r['missed_small_indices'].shape==(0,)
def geometry(m):
    r=m.diagnose_queries(np.ones((1,1)),np.array([[0.,0,.5,1]]),np.array([[0.,0,1,1],[.5,0,1,1]]),1,.5,1);assert_array_equal(r['missed_small_indices'],[1])
def invalid(m):
    for f,p,t in [(np.zeros((1,2)),np.array([[0.,0,1,1]]),np.empty((0,4))),(np.ones((1,2)),np.array([[0.,0,0,1]]),np.empty((0,4))),(np.ones((1,2)),np.array([[0.,0,1,1]]),np.array([[0.,0,2,1]]))]:
        with np.testing.assert_raises(ValueError):m.diagnose_queries(f,p,t,.9,.5,.1)
TESTS=[('Redundancy and missed object','public',example),('Absent queries','public',empty),('Cosine area and IoU equality','hidden',boundaries),('Partial overlap and touching boxes','hidden',geometry),('Validation','hidden',invalid)]

def scale_storage(m):
    features=np.ones((256,256))[:,::2];boxes=np.tile([0.,0.,1.,1.,0.,0.,1.,1.],(256,1))[:,0:4];targets=boxes[::2];saved=features.copy();r=m.diagnose_queries(features,boxes,targets,.9,1,1)
    expected=np.array([(i,j) for i in range(256) for j in range(i+1,256)],dtype=np.int64);assert_array_equal(r['similar_pairs'],expected);assert r['missed_small_indices'].shape==(0,);assert_array_equal(features,saved)
    for out in r.values():assert not np.shares_memory(out,features)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
