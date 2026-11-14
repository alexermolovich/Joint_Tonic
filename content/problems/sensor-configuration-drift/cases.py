import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
    y=np.array([[0.,0,0],[1,0,0]]);x=np.stack([y,y+[1,0,0]]);r=m.compare_drift(x,y,np.ones((2,2),bool),1);assert_allclose(r['rmse'],[0,1]);assert_allclose(r['endpoint'],[0,1]);assert_allclose(r['improvement'],[1,0]);assert r['best']==0
def missing(m):
    r=m.compare_drift(np.zeros((2,2,3)),np.zeros((2,3)),np.array([[True,False],[False,True]]),0);assert r['count']==0 and r['best']==-1;assert np.isnan(r['errors']).all();assert np.isnan(r['rmse']).all()
def oracle(m):
    rng=np.random.default_rng(852);x=rng.normal(size=(8,4096,6))[:,:,::2];y=rng.normal(size=(4096,3));mask=rng.random((8,4096))>.1;before=x.copy();out=m.compare_drift(x,y,mask,3);ids=[j for j in range(4096) if all(mask[:,j])];err=np.array([[sum(float(x[c,j,k]-y[j,k])**2 for k in range(3))**.5 for j in ids] for c in range(8)]);rmse=np.array([sum(row*row)/len(ids) for row in err])**.5;assert_allclose(out['errors'][:,ids],err);assert_allclose(out['rmse'],rmse);assert_allclose(out['endpoint'],err[:,-1]);assert_allclose(out['improvement'],rmse[3]-rmse);assert out['best']==int(np.argmin(rmse));assert_array_equal(x,before);assert not np.shares_memory(out['errors'],x)
def ties(m):
    x=np.zeros((2,3,3));x[:,0,0]=2;x[0,2,0]=100;mask=np.array([[True,True,False],[True,False,True]]);r=m.compare_drift(x,np.zeros((3,3)),mask,0);assert r['count']==1 and r['best']==0;assert_allclose(r['endpoint'],[2,2]);assert_allclose(r['rmse'],[2,2])
def invalid(m):
    x=np.zeros((1,1,3));y=np.zeros((1,3));v=np.ones((1,1),bool);bad(lambda:m.compare_drift(x,y,v,True));bad(lambda:m.compare_drift(x,y,v,1));x[:]=np.nan;bad(lambda:m.compare_drift(x,y,np.zeros((1,1),bool),0))
TESTS=[('Configuration improvement on common support','public',first),('No common evidence','public',missing),('Scalar Euclidean metric oracle at noncontiguous scale','hidden',oracle),('Coverage exclusion endpoint and stable ties','hidden',ties),('Invalid identity and masked numeric values','hidden',invalid)]
