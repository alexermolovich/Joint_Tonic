import numpy as np
from numpy.testing import assert_allclose
def example(m):
    d,j=m.prompt_class_drift(np.eye(2),np.array([[1.,0],[1,0]]),np.array([1,0],dtype=np.int64),np.array([0,1],dtype=np.int64));assert_allclose(d,[0,1]);assert_allclose(j,np.log(2))
def scales(m):
    d,j=m.prompt_class_drift(np.eye(2),np.eye(2)*3,np.array([1,3],dtype=np.int64),np.array([2,6],dtype=np.int64));assert_allclose(d,0,atol=1e-12);assert j==0
def symmetry(m):
    a=np.array([[1.,2],[-1,0],[2,3]]);b=np.array([[-2.,-4],[0,1],[2,3]]);x=np.array([3,0,7],dtype=np.int64);y=np.array([0,6,4],dtype=np.int64);d,j=m.prompt_class_drift(a,b,x,y);e,k=m.prompt_class_drift(b,a,y,x);assert_allclose(d,e);assert_allclose(j,k);assert_allclose(d,[2,1,0],atol=1e-12);assert 0<=j<=np.log(2)
def invalid(m):
    for a,b,x,y in [(np.zeros((1,1)),np.ones((1,1)),np.ones(1,dtype=np.int64),np.ones(1,dtype=np.int64)),(np.ones((1,1)),np.ones((1,1)),np.zeros(1,dtype=np.int64),np.ones(1,dtype=np.int64)),(np.ones((1,1)),np.ones((1,1)),np.ones(1),np.ones(1,dtype=np.int64))]:
        with np.testing.assert_raises(ValueError):m.prompt_class_drift(a,b,x,y)
TESTS=[('Independent drift channels','public',example),('Scale invariance','public',scales),('Symmetry and antipodal prompts','hidden',symmetry),('Validation','hidden',invalid)]

def scale_storage(m):
    rng=np.random.default_rng(119);a=rng.normal(size=(256,1024))[:,::2];b=a*2;counts=np.arange(512,dtype=np.int64)[::2];saved=a.copy();d,j=m.prompt_class_drift(a,b,counts,counts*2);assert_allclose(d,0,atol=1e-12);assert abs(j)<1e-12;assert not np.shares_memory(d,a);assert_allclose(a,saved)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
