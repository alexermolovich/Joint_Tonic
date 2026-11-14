"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def examples(m):
 a=np.array([[1.,2.,3.],[4.,5.,6.]]);mask=np.array([[True,False,True],[False,True,False]])
 out=m.mask_action_dimensions(a,mask);np.testing.assert_array_equal(out,[[1.,0.,3.],[0.,5.,0.]])
 assert out.dtype==np.float64 and not np.shares_memory(out,a)
def placeholders(m):
 out=m.mask_action_dimensions(np.array([[np.nan,0.,np.inf,-np.inf]]),np.array([[False,True,False,False]]))
 np.testing.assert_array_equal(out,np.zeros((1,4)))
def empty(m):
 out=m.mask_action_dimensions(np.empty((0,128)),np.empty((0,128),dtype=bool));assert out.shape==(0,128) and out.dtype==np.float64
def oracle(m):
 rng=np.random.default_rng(20261113);a=rng.normal(size=(1024,256))[:,::2];mask=rng.integers(0,2,(1024,256)).astype(bool)[:,::2]
 a[~mask]=np.nan;before=a.copy();bmask=mask.copy();out=m.mask_action_dimensions(a,mask)
 expected=np.zeros_like(a)
 for row in range(len(a)):
  for col in range(a.shape[1]):
   if mask[row,col]:expected[row,col]=a[row,col]
 np.testing.assert_array_equal(out,expected);assert out.dtype==np.float64
 assert not np.shares_memory(out,a) and not np.shares_memory(out,mask)
 np.testing.assert_array_equal(a,before);np.testing.assert_array_equal(mask,bmask)
def invalid(m):
 a=np.ones((1,2));mask=np.ones((1,2),dtype=bool)
 for x,y in [(a.tolist(),mask),(a,mask.tolist()),(a.astype(np.float32),mask),(a,mask.astype(int)),(a,np.ones((2,1),dtype=bool)),(a[0],mask),(np.ones((1025,2)),np.ones((1025,2),dtype=bool)),(np.ones((1,129)),np.ones((1,129),dtype=bool)),(np.empty((1,0)),np.empty((1,0),dtype=bool))]:rejects(lambda:m.mask_action_dimensions(x,y))
 for v in [np.nan,np.inf,-np.inf,1000001.]:rejects(lambda:m.mask_action_dimensions(np.array([[v,0.]]),mask))
 np.testing.assert_array_equal(m.mask_action_dimensions(np.array([[-1e6,1e6]]),mask),[[-1e6,1e6]])

TESTS=[('Different channels', 'public', examples), ('NaN placeholders do not leak', 'public', placeholders), ('Empty batch', 'hidden', empty), ('Independent scalar mask and noncontiguous scale', 'hidden', oracle), ('Typed contracts and bounds', 'hidden', invalid)]
