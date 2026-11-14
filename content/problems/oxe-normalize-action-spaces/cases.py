import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def example1(m):
    y,v=m.normalize_action_spaces([[[3,9],[5,8]]],[[True,False]],[[1,0]],[[2,1]]);assert_array_equal(y,[[[1,0],[2,0]]]);assert_array_equal(v,[[[True,False],[True,False]]])
def example2(m):
    y,v=m.normalize_action_spaces([[[2]],[[2]]],[[True],[True]],[[0],[2]],[[2],[1]]);assert_array_equal(y,[[[1]],[[0]]])
def scale_storage(m):
    a=np.ones((16,128,64))[:,:,::2];v=np.ones((16,32),dtype=bool);v[:,::2]=False;y,mask=m.normalize_action_spaces(a,v,np.zeros((16,32)),np.ones((16,32)));assert y.shape==a.shape;assert_array_equal(y[:,0],v.astype(float));assert not np.shares_memory(mask,v) and not np.shares_memory(y,a);assert a.all()
def invalid(m):
    good=[[[[1]]],[[True]],[[0]],[[1]]]
    for i,v in [(0,[[[np.nan]]]),(1,[[1]]),(2,[[0,0]]),(3,[[0]]),(3,[[1e-7]]),(1,[[False],[True]])]:
        args=good.copy();args[i]=v;bad(lambda:m.normalize_action_spaces(*args))
TESTS=[('Missing channel mask','public',example1),('Per-embodiment statistics','public',example2),('Scale storage and real zero semantics','hidden',scale_storage),('Invalid normalization contract','hidden',invalid)]
