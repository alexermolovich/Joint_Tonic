import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def cost(m):
    r=m.score_contact_outcomes(np.array([0.,1.]).reshape(2,1,1,1),np.zeros((1,1,1)),[[True]],[1,0],[True,True],.2);assert_array_equal(r['image_error'],[0,1]);assert_allclose(r['costs'],[.2,1]);assert r['best_index']==0
def tie(m):
    x=np.zeros((2,1,1,1));r=m.score_contact_outcomes(x,x[0],[[True]],[0,0],[True,True],1);assert r['best_index']==0
    r=m.score_contact_outcomes(x,x[0],[[True]],[0,0],[False,False],1);assert r['best_index']==-1 and np.isnan(r['costs']).all()
def scale(m):
    x=np.ones((64,64,128,3))[:,:,::2,:];g=np.zeros((64,64,3));roi=np.ones((64,64),bool);roi[:,::2]=False;v=np.ones(64,bool);v[0]=False;r=m.score_contact_outcomes(x,g,roi,np.zeros(64),v,0);assert_allclose(r['costs'][1:],1);assert r['best_index']==1;assert not np.shares_memory(r['costs'],x)
    r=m.score_contact_outcomes(np.empty((0,1,1,1)),np.zeros((1,1,1)),[[True]],[],np.empty(0,bool),0);assert r['best_index']==-1 and r['costs'].shape==(0,)
def invalid(m):
    for x,roi,v in [(np.zeros((1,1,1,1)),[[False]],[True]),(np.full((1,1,1,1),np.nan),[[True]],[False]),(np.full((1,1,1,1),2),[[True]],[False])]:bad(lambda:m.score_contact_outcomes(x,np.zeros((1,1,1)),roi,[0],v,1))
TESTS=[('Appearance and effort tradeoff','public',cost),('Ties and invalid candidates','public',tie),('Scale ROI denominator and empty population','hidden',scale),('Invalid masked predictions','hidden',invalid)]
