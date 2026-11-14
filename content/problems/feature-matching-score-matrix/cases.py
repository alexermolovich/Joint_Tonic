import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def scalar(m):
 assert_allclose(m.feature_scores(np.array([[2.],[3.]]),np.array([[4.]])),[[8],[12]])
def scaling(m):
 assert_allclose(m.feature_scores(np.ones((1,4)),np.ones((1,4))),[[2]])
def oracle(m):
 rng=np.random.default_rng(834);a=rng.normal(size=(256,64))[:,::2];b=rng.normal(size=(384,64))[:,::2];before=a.copy();r=m.feature_scores(a,b);expected=np.empty((256,384))
 for i in range(256):
  for j in range(384):expected[i,j]=sum(float(a[i,k])*float(b[j,k]) for k in range(32))/np.sqrt(32)
 assert_allclose(r,expected,atol=1e-12);assert_array_equal(a,before);assert not np.shares_memory(r,a)
def boundaries(m):
 assert m.feature_scores(np.empty((0,3)),np.ones((2,3))).shape==(0,2)
 assert m.feature_scores(np.ones((2,3)),np.empty((0,3))).shape==(2,0)
 assert_allclose(m.feature_scores(np.array([[-2.,0.],[0.,3.]]),np.eye(2)),[[-np.sqrt(2),0],[0,3/np.sqrt(2)]])
def invalid(m):
 for a,b in [(np.ones((1,2)),np.ones((1,3))),(np.ones((1,1),np.float32),np.ones((1,1))),(np.ones((1,1))*101,np.ones((1,1))),(np.ones((1,0)),np.ones((1,0))),(np.ones((600,1)),np.ones((600,1)))]:bad(lambda:m.feature_scores(a,b))
TESTS=[('Nonunit learned descriptors','public',scalar),('Channel scaling','public',scaling),('Independent channel-sum oracle at scale','hidden',oracle),('Empty sets signed features','hidden',boundaries),('Invalid descriptor dimensions','hidden',invalid)]
