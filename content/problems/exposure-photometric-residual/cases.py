import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def rz(a):
    c=np.cos(a);s=np.sin(a);return np.array([[c,-s,0],[s,c,0],[0,0,1.]])

def first(m):
 r=m.photometric_residual(np.array([.2]),np.array([.4]),np.array([.01,.02]),np.zeros(2),np.zeros(2),np.ones(1),.1);assert_array_equal(r['residual'],[0]);assert r['total']==0
def second(m):
 r=m.photometric_residual(np.zeros(1),np.array([.5]),np.ones(2),np.zeros(2),np.zeros(2),np.array([.5]),.1);assert_allclose(r['energy'],[.0225]);assert_allclose(r['target_gradient'],[.05])
def oracle(m):
 rng=np.random.default_rng(822);a=rng.random(131072)[::2];b=rng.random(131072)[::2];w=rng.random(131072)[::2];before=[a.copy(),b.copy(),w.copy()];t=np.array([.01,.03]);g=np.array([-.2,.3]);o=np.array([.1,-.1]);r=m.photometric_residual(a,b,t,g,o,w,.2)
 expected=[];grad=[]
 for i in range(0,len(a),37):
  error=(float(b[i])+.1)-3*np.exp(.5)*(float(a[i])-.1);value=.5*error*error if abs(error)<=.2 else .2*(abs(error)-.1);expected.append(w[i]*value);grad.append(w[i]*max(-.2,min(.2,error)))
 assert_allclose(r['energy'][::37],expected);assert_allclose(r['target_gradient'][::37],grad)
 for x,y in zip(before,[a,b,w]):assert_array_equal(x,y)
 assert not np.shares_memory(r['residual'],a)
def edges(m):
 r=m.photometric_residual(np.array([.2,.2,.2]),np.array([.1,.2,.3]),np.ones(2),np.zeros(2),np.zeros(2),np.ones(3),.1);assert_allclose(r['target_gradient'],[-.1,0,.1]);assert_allclose(r['energy'],[.005,0,.005])
 h=1e-6;args=[np.array([.3]),np.array([.4]),np.ones(2),np.zeros(2),np.zeros(2),np.array([.7]),.5];mid=m.photometric_residual(*args);args[1]=np.array([.4+h]);hi=m.photometric_residual(*args)['total'];args[1]=np.array([.4-h]);lo=m.photometric_residual(*args)['total'];assert_allclose((hi-lo)/(2*h),mid['target_gradient'][0],atol=1e-10)
 r=m.photometric_residual(np.empty(0),np.empty(0),np.ones(2),np.zeros(2),np.zeros(2),np.empty(0),1);assert r['total']==0
def invalid(m):
 good=[np.ones(1),np.ones(1),np.ones(2),np.zeros(2),np.zeros(2),np.ones(1),.1]
 for i,v in [(0,np.array([2.])),(2,np.array([0.,1.])),(3,np.array([11.,0.])),(5,np.array([-1.])),(6,0),(6,10**1000)]:
  a=good.copy();a[i]=v;bad(lambda:m.photometric_residual(*a))
TESTS=[('Exposure-compensated equality','public',first),('Weighted robust outlier','public',second),('Independent photometric scalar oracle at scale','hidden',oracle),('Huber boundary, derivative and empty data','hidden',edges),('Invalid calibration and samples','hidden',invalid)]
