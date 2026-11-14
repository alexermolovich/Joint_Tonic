import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
    p=np.tile(np.eye(4),(2,1,1));p[1,0,3]=2;r=m.relative_odometry(p,np.array([0.,2.]),np.array([[0,1]],np.int64));assert_allclose(r['transforms'][0,:3,3],[2,0,0]);assert_allclose(r['durations'],[2]);assert_allclose(r['speeds'],[1])
def turned(m):
    p=np.tile(np.eye(4),(2,1,1));p[0,:3,:3]=[[0,-1,0],[1,0,0],[0,0,1]];p[1,0,3]=1;r=m.relative_odometry(p,np.array([0.,1.]),np.array([[0,1]],np.int64));assert_allclose(r['transforms'][0],np.linalg.inv(p[0])@p[1]);assert_allclose(r['transforms'][0,:3,3],[0,-1,0])
def oracle(m):
    rng=np.random.default_rng(850);p=np.tile(np.eye(4),(4096,1,1))[::2];a=rng.uniform(-3,3,len(p));p[:,0,0]=p[:,1,1]=np.cos(a);p[:,0,1]=-np.sin(a);p[:,1,0]=np.sin(a);p[:,:3,3]=rng.normal(size=(len(p),3));time=np.arange(len(p),dtype=float)*.01;e=np.array([[i,i+1] for i in range(len(p)-1)]+[[0,2000],[0,2000]],np.int64);old=p.copy();r=m.relative_odometry(p,time,e)
    expected=np.array([np.linalg.solve(p[i],p[j]) for i,j in e]);assert_allclose(r['transforms'],expected,atol=1e-10);assert_allclose(r['speeds'],[np.linalg.norm(p[j,:3,3]-p[i,:3,3])/(time[j]-time[i]) for i,j in e]);assert_array_equal(p,old);assert not np.shares_memory(p,r['transforms'])
def empty(m):
    r=m.relative_odometry(np.eye(4)[None],np.zeros(1),np.empty((0,2),np.int64));assert r['transforms'].shape==(0,4,4);assert r['speeds'].shape==(0,)
def invalid(m):
    p=np.tile(np.eye(4),(2,1,1));bad(lambda:m.relative_odometry(p,np.zeros(2),np.array([[0,1]],np.int64)));bad(lambda:m.relative_odometry(p,np.arange(2,dtype=float),np.array([[1,0]],np.int64)));p[0,0,0]=-1;bad(lambda:m.relative_odometry(p,np.arange(2,dtype=float),np.array([[0,1]],np.int64)))
TESTS=[('Translation and elapsed time','public',first),('Body-frame displacement after rotation','public',turned),('Homogeneous solve oracle at strided scale','hidden',oracle),('No selected edges','hidden',empty),('Invalid time edge and rigid transform','hidden',invalid)]
