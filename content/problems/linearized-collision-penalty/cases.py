import numpy as np
from numpy.testing import assert_allclose,assert_array_equal
def first(m):
 r=m.linearized_collision_penalty(np.array([.02,.08]),np.array([[1.],[-1.]]),np.array([.01]),.05);assert_allclose(r['predicted'],[.03,.07]);assert_allclose(r['hinge'],[.02,0]);assert_allclose(r['cost'],.02);assert_array_equal(r['gradient'],[-1])
def kink(m):
 r=m.linearized_collision_penalty(np.array([.05]),np.array([[2.]]),np.array([0.]),.05);assert r['cost']==0;assert_array_equal(r['gradient'],[0])
def derivative(m):
 d=np.array([-.3,.7,.1]);j=np.array([[1.,2.],[-1.,3.],[2.,-1.]]);s=np.array([.02,.01]);r=m.linearized_collision_penalty(d,j,s,.2)
 for k in range(2):
  e=np.zeros(2);e[k]=1e-6;grad=(m.linearized_collision_penalty(d,j,s+e,.2)['cost']-m.linearized_collision_penalty(d,j,s-e,.2)['cost'])/2e-6;assert_allclose(grad,r['gradient'][k],atol=1e-8)
def scale(m):
 j=np.ones((4096,32))[:,::2];d=np.zeros(4096);s=np.zeros(16);r=m.linearized_collision_penalty(d,j,s,1);assert r['cost']==4096;assert_array_equal(r['gradient'],np.full(16,-4096));r=m.linearized_collision_penalty(np.empty(0),np.empty((0,16)),s,1);assert r['cost']==0 and r['predicted'].shape==(0,);assert_array_equal(r['gradient'],np.zeros(16))
def invalid(m):
 with np.testing.assert_raises(ValueError):m.linearized_collision_penalty(np.ones(1),np.ones((1,2)),np.zeros(1),1)
 with np.testing.assert_raises(ValueError):m.linearized_collision_penalty(np.ones(1),np.ones((1,1)),np.zeros(1),10**1000)
TESTS=[('Local clearance update','public',first),('Chosen hinge subgradient','public',kink),('Finite difference local gradient','hidden',derivative),('Scale and empty constraints','hidden',scale),('Invalid model contract','hidden',invalid)]
