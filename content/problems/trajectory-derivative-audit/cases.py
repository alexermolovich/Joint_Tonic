import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def data():return [np.array([[2.]]),np.array([[-3.]]),np.array([[4.]]),np.array([[2.],[3.],[4.]])]
def first(m):
 r=m.audit_derivatives(*data());assert not r['violations'].any();assert_array_equal(r['max_ratio'],np.ones((3,1)));assert r['passed'] is True
def second(m):
 a=data();a[0][0,0]=2.2;r=m.audit_derivatives(*a);assert_array_equal(r['violations'],[[[True,False,False]]]);assert_allclose(r['max_ratio'][:,0],[1.1,1,1]);assert not r['passed']
def empty(m):
 z=np.empty((0,2));r=m.audit_derivatives(z,z,z,np.ones((3,2)));assert r['violations'].shape==(0,2,3) and not r['passed'];assert_array_equal(r['max_ratio'],np.zeros((3,2)))
def scale(m):
 rng=np.random.default_rng(800);v=rng.normal(size=(4096,32))[:,::2];a=v*2;j=v*3;lim=np.ones((3,16));r=m.audit_derivatives(v,a,j,lim);assert_array_equal(r['violations'][:,:,0],np.abs(v)>1);assert_allclose(r['max_ratio'][2],3*np.max(np.abs(v),axis=0));assert not np.shares_memory(r['violations'],v)
def invalid(m):
 a=data();a[3][0,0]=0
 with np.testing.assert_raises(ValueError):m.audit_derivatives(*a)
 a=data();a[1]=np.zeros((2,1))
 with np.testing.assert_raises(ValueError):m.audit_derivatives(*a)
TESTS=[('Inclusive limits','public',first),('Velocity violation','public',second),('Empty evidence','hidden',empty),('Scale and derivative axes','hidden',scale),('Invalid limits and shape','hidden',invalid)]
