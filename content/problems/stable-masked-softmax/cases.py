"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def large(m):np.testing.assert_array_equal(m.stable_masked_softmax(np.array([[1000.,1000.,-1000.]]),np.array([[True,True,False]])),[[.5,.5,0]])
def missing(m):np.testing.assert_array_equal(m.stable_masked_softmax(np.array([[1.,2.],[5.,9.]]),np.array([[False,False],[True,False]])),[[0,0],[1,0]])
def extremes(m):
 x=np.array([[-10000.,10000.],[10000.,-10000.]]);mask=np.array([[True,False],[False,True]]);np.testing.assert_array_equal(m.stable_masked_softmax(x,mask),[[1,0],[0,1]])
 r=m.stable_masked_softmax(np.empty((2,0)),np.empty((2,0),dtype=bool));assert r.shape==(2,0) and r.dtype==np.float64
def scale_oracle(m):
 rng=np.random.default_rng(9);x=rng.uniform(-10,10,(128,2048))[:,::2];mask=rng.random(x.shape)>.2;xc=x.copy();mc=mask.copy();r=m.stable_masked_softmax(x,mask)
 import math
 for b in [0,1,127]:
  den=math.fsum(math.exp(float(x[b,j])) for j in range(1024) if mask[b,j]);expected=[math.exp(float(x[b,j]))/den if mask[b,j] else 0. for j in range(1024)];np.testing.assert_allclose(r[b],expected,rtol=1e-12,atol=1e-14)
 np.testing.assert_allclose(r.sum(axis=1),1);assert not r[~mask].any() and not np.shares_memory(r,x);np.testing.assert_array_equal(x,xc);np.testing.assert_array_equal(mask,mc)
 np.testing.assert_allclose(m.stable_masked_softmax(x+100,mask),r,atol=1e-13)
def invalid(m):
 for x,v in [(np.array([[1]],dtype=np.int64),np.ones((1,1),bool)),(np.array([[np.nan]]),np.zeros((1,1),bool)),(np.zeros((1,1)),np.ones((1,1))), (np.zeros((0,1)),np.zeros((0,1),bool)),(np.full((1,1),10001.),np.ones((1,1),bool)),(np.zeros((1,2049)),np.ones((1,2049),bool))]:rejects(lambda:m.stable_masked_softmax(x,v))

TESTS=[('Overflow-safe equal evidence', 'public', large), ('All missing and one valid token', 'public', missing), ('Masked maximum and empty token axis', 'hidden', extremes), ('Independent scalar probability oracle and scale', 'hidden', scale_oracle), ('Invalid score schema', 'hidden', invalid)]
