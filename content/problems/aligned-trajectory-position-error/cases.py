import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

P=np.array([[0.,0.,0.],[1,0,0],[0,1,0],[0,0,1]])
R=np.array([[0.,-1,0],[1,0,0],[0,0,1.]])
def similarity(m):
 y=2*(P@R.T)+[1,2,3];r=m.align_trajectory(P,y,True);assert_allclose(r['rotation'],R,atol=1e-12);assert_allclose(r['translation'],[1,2,3],atol=1e-12);assert_allclose(r['scale'],2);assert r['rmse']<1e-12
def rigid(m):
 y=2*(P@R.T)+[1,2,3];r=m.align_trajectory(P,y,False);assert r['scale']==1;assert_allclose(r['rotation'],R,atol=1e-12);assert_allclose(r['rmse'],.75);assert_allclose(r['translation'],np.array([1,2,3])+R@P.mean(axis=0),atol=1e-12)
def oracle(m):
 rng=np.random.default_rng(849);x=rng.normal(size=(4096,6))[:,::2]+[10,-20,3];q,_=np.linalg.qr(rng.normal(size=(3,3)));q[:,0]*=np.linalg.det(q);s=1.7;t=np.array([3.,4.,5.]);y=np.array([s*(q@p)+t for p in x]);before=x.copy();r=m.align_trajectory(x,y,True);assert_allclose(r['rotation'],q,atol=1e-12);assert_allclose(r['translation'],t,atol=1e-12);assert_allclose(r['scale'],s,atol=1e-12);assert_allclose(r['aligned'],y,atol=1e-12);assert r['rmse']<1e-11;assert_array_equal(x,before);assert not np.shares_memory(r['aligned'],x)
 # Residual error is measured by Euclidean norm, not per-coordinate RMSE.
 y=y+rng.normal(scale=.01,size=y.shape);r=m.align_trajectory(x,y,False);errors=[sum(float(v)**2 for v in a-b)**.5 for a,b in zip(r['aligned'],y)];assert_allclose(r['errors'],errors);assert_allclose(r['rmse'],(sum(e*e for e in errors)/len(errors))**.5);assert_allclose(r['rotation'].T@r['rotation'],np.eye(3),atol=1e-12)
def reflection(m):
 x=np.array([[1.,1.,1.],[1,-1,-1],[-1,1,-1],[-1,-1,1]]);y=x*np.array([-1.,1.,1.]);r=m.align_trajectory(x,y,False);assert_allclose(np.linalg.det(r['rotation']),1,atol=1e-12);assert_allclose(r['rmse'],2)
 x=np.array([[0.,0.,0.],[1,0,0],[0,1,0]]);r=m.align_trajectory(x,x,True);assert r['rmse']<1e-12
def invalid(m):
 for x,y,s in [(np.zeros((3,3)),np.zeros((3,3)),True),(np.array([[0.,0,0],[1,0,0],[2,0,0]]),np.eye(3),True),(P,P,1),(P.astype(np.float32),P,True)]:bad(lambda:m.align_trajectory(x,y,s))
TESTS=[('Known similarity alignment','public',similarity),('Metric rigid alignment preserves scale discrepancy','public',rigid),('Known nontrivial frame transform and scalar error oracle at scale','hidden',oracle),('Physical rotation rejects mirror alignment','hidden',reflection),('Invalid degenerate clouds and scale mode','hidden',invalid)]
