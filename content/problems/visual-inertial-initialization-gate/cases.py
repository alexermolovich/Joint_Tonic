import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def args():return [1.,np.array([0.,0.,-9.81]),np.zeros(3),np.zeros(3),np.array([.2]),np.ones(1,bool),np.ones((1,1)),np.array([.5,2,.1,.1,.1,.2,1e-6])]
def first(m):
    r=m.validate_initialization(*args());assert r['accepted'] and r['rank']==1;assert_array_equal(r['checks'],np.ones(6,bool));assert_allclose(r['rms'],.2)
def deficient(m):
    a=args();a[4]=np.zeros(2);a[5]=np.ones(2,bool);a[6]=np.array([[1.,0],[1,0]]);r=m.validate_initialization(*a);assert not r['accepted'] and r['rank']==1;assert_array_equal(r['checks'],[False,True,True,True,True,True])
def oracle(m):
    rng=np.random.default_rng(857);j=rng.normal(size=(4096,64))[:,::2];r=rng.normal(size=4096)*.1;mask=np.arange(4096)%3!=0;a=args();a[4:7]=[r,mask,j];before=j.copy();out=m.validate_initialization(*a);assert out['accepted'] and out['rank']==32;assert_allclose(out['rms'],(sum(float(x*x) for x in r[mask])/mask.sum())**.5);assert_array_equal(j,before);assert not np.shares_memory(out['checks'],mask)
    a=args();a[0]=3;a[1]=np.zeros(3);a[2]=np.ones(3);a[3]=np.ones(3);a[4]=np.ones(1);out=m.validate_initialization(*a);assert_array_equal(out['checks'],[True,False,False,False,False,False]);assert not out['accepted']
def empty_boundary(m):
    a=args();a[4]=np.empty(0);a[5]=np.empty(0,bool);a[6]=np.empty((0,2));r=m.validate_initialization(*a);assert r['count']==0 and r['rank']==0 and np.isnan(r['rms']);assert_array_equal(r['checks'],[False,True,True,True,True,False]);a=args();a[0]=.5;a[2][0]=.1;a[3][0]=.1;assert m.validate_initialization(*a)['accepted'];a[4]=np.zeros(2);a[5]=np.ones(2,bool);a[6]=np.diag([1.,1e-6]);assert m.validate_initialization(*a)['rank']==1
def invalid(m):
    for index,value in [(0,10**1000),(4,np.array([np.nan])),(7,np.array([2.,1,.1,.1,.1,.2,1e-6])),(6,np.ones((1,0)))]:
        a=args();a[index]=value;bad(lambda:m.validate_initialization(*a))
TESTS=[('Observable physically plausible candidate','public',first),('Perfect fit with unobservable scale direction','public',deficient),('Independent RMS oracle scale and isolated failure flags','hidden',oracle),('No evidence inclusive limits and strict rank cutoff','hidden',empty_boundary),('Invalid scalar shape and limit interval','hidden',invalid)]
