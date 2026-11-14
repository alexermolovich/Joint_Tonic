"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def mask(m):
 r=m.broadcast_sensor_features(np.array([[[2.],[3.]]]),np.array([[9.]]),np.array([[True,False]]));np.testing.assert_array_equal(r,[[[2,9],[0,0]]])
def batch(m):np.testing.assert_array_equal(m.broadcast_sensor_features(np.array([[[1.]],[[2.]]]),np.array([[10.,11.],[20.,21.]]),np.ones((2,1),dtype=bool)),[[[1,10,11]],[[2,20,21]]])
def empty(m):
 x=np.empty((2,0,3));c=np.zeros((2,4));r=m.broadcast_sensor_features(x,c,np.empty((2,0),dtype=bool));assert r.shape==(2,0,7) and r.dtype==np.float64
 r=m.broadcast_sensor_features(np.zeros((1,1,1)),np.array([[2.]]),np.ones((1,1),dtype=bool));np.testing.assert_array_equal(r,[[[0,2]]])
def scale(m):
 x=np.arange(32*128*64,dtype=float).reshape(32,128,64)[:,:,::2];c=np.arange(32*32,dtype=float).reshape(32,32);p=np.ones((32,256),dtype=bool)[:,::2];p[:,::3]=False;xc=x.copy();cc=c.copy();r=m.broadcast_sensor_features(x,c,p)
 for b,t in [(0,0),(31,127),(20,60),(7,8)]:np.testing.assert_array_equal(r[b,t],np.r_[x[b,t],c[b]] if p[b,t] else np.zeros(64))
 assert r.shape==(32,128,64) and not np.shares_memory(r,x);np.testing.assert_array_equal(x,xc);np.testing.assert_array_equal(c,cc)
def invalid(m):
 good=[np.ones((1,1,1)),np.ones((1,1)),np.ones((1,1),dtype=bool)]
 for i,value in [(0,np.ones((1,1,1),dtype=np.float32)),(0,np.full((1,1,1),np.nan)),(1,np.ones((2,1))),(2,np.ones((1,1))),(0,np.ones((1,257,1))),(1,np.ones((1,0)))]:
  a=[v.copy() for v in good];a[i]=value;rejects(lambda:m.broadcast_sensor_features(*a))

TESTS=[('Mask whole sensor context row', 'public', mask), ('Distinct robot contexts', 'public', batch), ('Empty horizon and real zero observation', 'hidden', empty), ('Noncontiguous robot batch alignment', 'hidden', scale), ('Invalid episode schema', 'hidden', invalid)]
