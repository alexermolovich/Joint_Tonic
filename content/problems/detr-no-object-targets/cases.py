import numpy as np
from numpy.testing import assert_array_equal


def padded(m):
    c,w=m.build_query_targets(np.array([[2,0]],dtype=np.int64),np.array([[True,False]]),np.array([[0,-1]],dtype=np.int64),3,.1)
    assert_array_equal(c,[[2,3]]);assert_array_equal(w,[[1,.1]])


def reordered(m):
    c,w=m.build_query_targets(np.array([[1,0]],dtype=np.int64),np.ones((1,2),dtype=bool),np.array([[1,-1,0]],dtype=np.int64),2,.2)
    assert_array_equal(c,[[0,2,1]]);assert_array_equal(w,[[1,.2,1]])


def no_targets(m):
    c,w=m.build_query_targets(np.empty((2,0),dtype=np.int64),np.empty((2,0),dtype=bool),np.full((2,3),-1,dtype=np.int64),4,0)
    assert_array_equal(c,np.full((2,3),4));assert_array_equal(w,np.zeros((2,3)))


def independent_batches(m):
    l=np.array([[0,1,2],[2,1,0]],dtype=np.int64);v=np.array([[True,True,False],[False,True,True]]);j=np.array([[1,0,-1],[2,-1,1]],dtype=np.int64)
    old=[x.copy() for x in (l,v,j)]
    c,w=m.build_query_targets(l,v,j,3,.5)
    assert_array_equal(c,[[1,0,3],[0,3,1]]);assert_array_equal(w,[[1,1,.5],[1,.5,1]])
    for x,y in zip((l,v,j),old):assert_array_equal(x,y);assert not np.shares_memory(c,x)
    assert c.dtype==np.int64 and w.dtype==np.float64


def invalid(m):
    l=np.array([[0,1]],dtype=np.int64);v=np.ones((1,2),dtype=bool)
    with np.testing.assert_raises(TypeError):m.build_query_targets([],v,np.array([[-1]],dtype=np.int64),2,.1)
    for labels,valid,matches,c,e in [(l,v,np.array([[0,0]],dtype=np.int64),2,.1),(l,np.array([[True,False]]),np.array([[1]],dtype=np.int64),2,.1),(l,v,np.array([[2]],dtype=np.int64),2,.1),(l,v,np.array([[-2]],dtype=np.int64),2,.1),(l,v,np.array([[0]],dtype=np.int64),1,.1),(l,v,np.array([[0]],dtype=np.int64),2,float('nan')),(l.astype(np.int32),v,np.array([[0]],dtype=np.int64),2,.1)]:
        with np.testing.assert_raises(ValueError):m.build_query_targets(labels,valid,matches,c,e)


TESTS=[("Padded targets and unused query","public",padded),("Query versus target order","public",reordered),("No target annotations","public",no_targets),
       ("Independent batched assignments","hidden",independent_batches),("Assignment validation","hidden",invalid)]
