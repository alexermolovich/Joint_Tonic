import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.masked_action_flow_loss([[[0,9]]],[[[3,7]]],[[[1,2]]],[[[True,False]]]);assert r['loss']==4;assert_allclose(r['per_example'],[4]);assert_array_equal(r['gradient'],[[[-4,0]]])
def unsupported(m):
    r=m.masked_action_flow_loss([[[2]]],[[[7]]],[[[1]]],[[[False]]]);assert r['loss']==0 and r['per_example'][0]==0 and r['gradient'][0,0,0]==0

def scale(m):
    v=np.zeros((32,64,64))[:,:,::2];a=np.ones_like(v)*3;e=np.ones_like(v);mask=np.ones_like(v,dtype=bool);mask[0]=False;r=m.masked_action_flow_loss(v,a,e,mask);assert r['loss']==4;assert r['per_example'][0]==0;assert_allclose(r['gradient'][1:],-4/(31*64*32));assert not r['gradient'][0].any()
    r=m.masked_action_flow_loss([[[0,0]],[[0,0]]],[[[1,1]],[[3,0]]],np.zeros((2,1,2)),[[[True,True]],[[True,False]]]);assert_allclose(r['loss'],11/3);assert_allclose(r['per_example'],[1,9])
def invalid(m):
    for a in [([[[1]]],[[[1]]],[[[1]]],[[[1]]]),([[[1]]],[[[1,2]]],[[[1]]],[[[True]]]),([[[np.nan]]],[[[1]]],[[[1]]],[[[False]]])]:bad(lambda:m.masked_action_flow_loss(*a))
TESTS=[('Velocity target and gradient','public',one),('No supervised action entries','public',unsupported),('Scale and global support weighting','hidden',scale),('Invalid flow tensors','hidden',invalid)]
