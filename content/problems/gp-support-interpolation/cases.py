import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
 r=m.interpolate_support(np.array([[0.,0]]),np.array([[1.,0]]),2,np.array([.5]));assert_allclose(r['position'],[[.5]]);assert_allclose(r['velocity'],[[.75]])
def second(m):
 r=m.interpolate_support(np.array([[0.,2]]),np.array([[4.,2]]),2,np.array([0.,.5,1.]));assert_allclose(r['position'],[[0],[2],[4]]);assert_allclose(r['velocity'],[[2],[2],[2]])
def oracle(m):
 rng=np.random.default_rng(815);a=rng.normal(size=(16,4))[:,::2];b=rng.normal(size=(16,4))[:,::2];u=np.linspace(1,0,8192)[::2];before=[a.copy(),b.copy(),u.copy()];t=.7;r=m.interpolate_support(a,b,t,u)
 # Solve independent elapsed-time polynomial boundary equations.
 mat=np.array([[t*t,t**3],[2*t,3*t*t]])
 c=np.linalg.solve(mat,np.stack([b[:,0]-a[:,0]-t*a[:,1],b[:,1]-a[:,1]]))
 time=t*u[:,None];expected=a[:,0]+a[:,1]*time+c[0]*time**2+c[1]*time**3
 assert_allclose(r['position'],expected,atol=1e-12);assert_allclose(r['velocity'],a[:,1]+2*c[0]*time+3*c[1]*time**2,atol=1e-12)
 for x,y in zip(before,[a,b,u]):assert_array_equal(x,y)
 assert not np.shares_memory(r['position'],a)
def boundaries(m):
 a=np.array([[1.,3.]]);b=np.array([[-2.,4.]]);r=m.interpolate_support(a,b,.001,np.array([1.,0.]));assert_allclose(r['position'],[[-2],[1]]);assert_allclose(r['velocity'],[[4],[3]])
 assert m.interpolate_support(a,b,1,np.empty(0))['position'].shape==(0,1)
def invalid(m):
 for t in [0,1e-4,101,True,10**1000]:bad(lambda:m.interpolate_support(np.zeros((1,2)),np.zeros((1,2)),t,np.zeros(1)))
 bad(lambda:m.interpolate_support(np.zeros((1,2)),np.zeros((1,2)),1,np.array([1.1])))
 bad(lambda:m.interpolate_support(np.zeros((0,2)),np.zeros((0,2)),1,np.zeros(1)))
TESTS=[('Rest endpoints','public',first),('Constant velocity interval','public',second),('Independent polynomial oracle at scale','hidden',oracle),('Endpoint and empty queries','hidden',boundaries),('Invalid support interval','hidden',invalid)]
