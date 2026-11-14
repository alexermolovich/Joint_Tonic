import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):assert_array_equal(m.group_attention_mask([0,1],[[True,False],[True,True]],[[True,True]]),[[[1,0],[1,1]]])
def missing(m):assert_array_equal(m.group_attention_mask([0,1],[[True,False],[True,True]],[[False,True]]),[[[0,0],[0,1]]])
def scale(m):
    ids=np.arange(512)[::2]%3;r=np.eye(3,dtype=bool);p=np.ones((8,512),bool)[:,::2];p[:,::7]=False;a=m.group_attention_mask(ids,r,p);assert a.shape==(8,256,256);assert_array_equal(a[0],(ids[:,None]==ids[None,:])&p[0,:,None]&p[0,None,:]);assert m.group_attention_mask(np.array([],int),r,np.empty((1,0),bool)).shape==(1,0,0)
def invalid(m):
    for a in [([1],[[True]],[[True]]),([0],[[1]],[[True]]),([0],[[True]],[[True,False]]),([0.],[[True]],[[True]])]:bad(lambda:m.group_attention_mask(*a))
TESTS=[('Directed group rules','public',one),('Missing goal','public',missing),('Scale empty and noalias','hidden',scale),('Invalid rules','hidden',invalid)]
