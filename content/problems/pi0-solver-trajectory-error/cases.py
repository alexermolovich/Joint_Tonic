import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.solver_trajectory_error([[[1]],[[0]]],[[0]],[1,4],[2,4],.5,4);assert_allclose(r['rmse'],[1,0]);assert_array_equal(r['feasible'],[False,True]);assert r['selected_index']==1

def ties(m):assert m.solver_trajectory_error([[[0]],[[0]]],[[0]],[4,2],[3,3],0,3)['selected_index']==1

def scale(m):
    x=np.ones((64,256,32))[:,:,::2];r=m.solver_trajectory_error(x,np.zeros((256,16)),np.arange(1,65),np.arange(64),1,0);assert np.all(r['rmse']==1) and np.all(r['max_abs_error']==1) and r['selected_index']==0;assert m.solver_trajectory_error([[[1]]],[[0]],[1],[1],0,1)['selected_index']==-1

def invalid(m):
    for a in [([[[1]]],[[0]],[0],[1],1,1),([[[1]]],[[0]],[1],[-1],1,1),([[[1]]],[[0]],[1],[1],True,1)]:bad(lambda:m.solver_trajectory_error(*a))
TESTS=[('Error versus measured deadline','public',one),('Deterministic tie order','public',ties),('Scale and no feasible option','hidden',scale),('Invalid solver records','hidden',invalid)]
