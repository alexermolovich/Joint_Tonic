import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.label_interventions([[.1],[.2],[.3]],[[.9],[.8],[.7]],[False,True,True],[0,0,0]);assert_allclose(r['executed_actions'],[[.1],[.8],[.7]]);assert_array_equal(r['segment_id'],[-1,0,0]);assert_array_equal(r['segments'],[[0,1,3]])
def episodes(m):
    r=m.label_interventions([[0],[0]],[[1],[1]],[True,True],[0,1]);assert_array_equal(r['segments'],[[0,0,1],[1,1,2]]);assert_array_equal(r['segment_id'],[0,1])
def scale(m):
    p=np.zeros((16384,32))[:,::2];h=np.ones_like(p);mask=np.arange(16384)%4>=2;ep=np.arange(16384)//64;before=p.copy();r=m.label_interventions(p,h,mask,ep);starts=np.arange(2,16384,4);assert_array_equal(r['segments'],np.column_stack([ep[starts],starts,starts+2]));assert_array_equal(r['executed_actions'][:,0],mask.astype(float));assert_array_equal(p,before);assert not np.shares_memory(r['executed_actions'],p)
    r=m.label_interventions(np.empty((0,1)),np.empty((0,1)),np.empty(0,bool),np.empty(0,int));assert r['segments'].shape==(0,3)
    r=m.label_interventions([[0]],[[1]],[False],[0]);assert r['segments'].shape==(0,3) and r['segment_id'][0]==-1

def invalid(m):
    for p,h,mask,ep in [([[0]],[[2]],[False],[0]),([[0]],[[0]],[1],[0]),([[0],[0]],[[0],[0]],[True,True],[1,0]),([[0]],[[np.nan]],[False],[0])]:bad(lambda:m.label_interventions(p,h,mask,ep))
TESTS=[('Executed commands and one correction run','public',one),('Human run split by episode','public',episodes),('Exact run intervals noncontiguous scale and empty traces','hidden',scale),('Invalid even unselected commands','hidden',invalid)]
