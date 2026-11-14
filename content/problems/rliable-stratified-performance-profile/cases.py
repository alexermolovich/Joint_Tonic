"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import math
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')

def same(a,b):np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)
def f(x):return np.array(x,dtype=np.float64)
def i(x):return np.array(x,dtype=np.int64)
def b(x):return np.array(x,dtype=bool)

def unchanged(before,after):
    for x,y in zip(before,after):np.testing.assert_array_equal(x,y)

def example1(m):
 r=m.stratified_profile(f([[0,2],[10,12]]),f([2,10]),i([[[1,1],[0,0]]]))
 same(r['profile'],[.5,.25]);same(r['replicates'],[[.5,0]])
def example2(m):
 r=m.stratified_profile(f([[1]]),f([1,0,1]),np.zeros((0,1,1),dtype=np.int64));same(r['profile'],[0,1,0]);assert r['replicates'].shape==(0,3)
def edges(m):
 r=m.stratified_profile(np.ones((2,3),dtype=np.float32),f([]),np.zeros((4,2,3),dtype=np.int64));assert r['profile'].shape==(0,) and r['replicates'].shape==(4,0)
 r=m.stratified_profile(f([[0],[2]]),f([0,1,2]),i([[[0],[0]],[[0],[0]]]))
 same(r['replicates'],[[.5,.5,0],[.5,.5,0]]);assert r['replicates'].dtype==np.float64
def oracle_scale(m):
 rng=np.random.default_rng(921);x=rng.normal(size=(32,128))[:,::2];t=f([0,-1,1,0]);idx=rng.integers(0,64,size=(64,32,128),dtype=np.int64)[:,:,::2];before=[v.copy() for v in [x,t,idx]]
 r=m.stratified_profile(x,t,idx);expected=[]
 for block in idx:
  values=[float(x[row,int(col)]) for row,cols in enumerate(block) for col in cols]
  expected.append([sum(value>threshold for value in values)/len(values) for threshold in t])
 same(r['replicates'],expected);same(r['profile'],[sum(float(v)>q for v in x.ravel())/x.size for q in t]);unchanged(before,[x,t,idx])
def invalid(m):
 for x,t,idx in [(f([[0]]),f([0]),i([[[1]]])),(f([[0]]),f([0]),i([[[-1]]])),(f([[0]]),f([np.nan]),i([[[0]]])),(f([[np.inf]]),f([0]),i([[[0]]])),(f([[0]]),f([0]),f([[[0]]])),(f([[0]]),f([0]),np.zeros((1,2,1),dtype=np.int64)),(np.zeros((0,1)),f([]),np.zeros((0,0,1),dtype=np.int64)),(np.zeros((128,128)),np.zeros(128),np.zeros((16,128,128),dtype=np.int64))]:reject(lambda:m.stratified_profile(x,t,idx))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
