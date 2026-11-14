import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def blend(m):
    r=m.combine_motion_rewards([[.8]],[[.2]],[[True]],.75,.25);assert_allclose(r['motion_contribution'],[[.6]]);assert_allclose(r['task_contribution'],[[.05]]);assert_allclose(r['mean_reward'],.65)
def zero(m):
    r=m.combine_motion_rewards([[.8]],[[.2]],[[True]],0,0);assert r['mean_reward']==0
    r=m.combine_motion_rewards([[.8]],[[.2]],[[False]],1,1);assert r['mean_reward']==0 and r['reward'][0,0]==0
def scale(m):
    a=np.ones((128,512))[:,::2];mask=np.ones_like(a,bool);mask[:,::2]=False;r=m.combine_motion_rewards(a,a,mask,2,3);assert r['mean_reward']==5;assert_array_equal(r['reward'],mask*5);assert not np.shares_memory(r['reward'],a);assert not np.shares_memory(r['motion_contribution'],r['reward'])
def invalid(m):
    for args in [([[2]],[[0]],[[True]],1,1),([[1]],[[0]],[[1]],1,1),([[1]],[[0]],[[True]],-1,1),([[1]],[[0]],[[True]],10**1000,1)]:bad(lambda:m.combine_motion_rewards(*args))
TESTS=[('Weighted motion and goal','public',blend),('Zero weights and absent evidence','public',zero),('Scale independent contributions','hidden',scale),('Invalid rewards','hidden',invalid)]
