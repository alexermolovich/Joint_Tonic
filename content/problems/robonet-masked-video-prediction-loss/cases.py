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
 p=f([.2,.8,np.nan,np.inf]).reshape(1,2,1,2,1);y=f([0,1,np.nan,np.inf]).reshape(p.shape);r=m.masked_video_loss(p,y,b([[True,False]]));same(r['loss'],.04);same(r['per_horizon'],[.04,np.nan]);same(r['frame_counts'],[1,0]);assert r['has_data'] is True
def example2(m):
 p=f([[0,1],[1,np.nan]]).reshape(2,2,1,1,1);r=m.masked_video_loss(p,np.zeros_like(p),b([[True,True],[True,False]]));same(r['loss'],2/3);same(r['per_horizon'],[.5,1]);same(r['frame_counts'],[2,1])
def edges(m):
 p=np.full((2,2,1,1,3),np.nan,dtype=np.float32);r=m.masked_video_loss(p,p.copy(),np.zeros((2,2),dtype=bool));assert r['loss']==0 and r['has_data'] is False and np.isnan(r['per_horizon']).all();assert r['frame_counts'].dtype==np.int64
 r=m.masked_video_loss(np.zeros((0,1,1,1,1)),np.zeros((0,1,1,1,1)),np.zeros((0,1),dtype=bool));assert r['loss']==0
def oracle_scale(m):
 rng=np.random.default_rng(935);p=rng.uniform(size=(32,8,16,32,3))[:,:,:,::2,:];y=rng.uniform(size=p.shape);mask=rng.uniform(size=(32,8))>.2;before=[v.copy() for v in [p,y,mask]];r=m.masked_video_loss(p,y,mask);errors=[];by_time=[[] for _ in range(8)]
 for batch in range(32):
  for t in range(8):
   if mask[batch,t]:
    value=math.fsum((float(a)-float(b))**2 for a,b in zip(p[batch,t].ravel(),y[batch,t].ravel()))/(16*16*3);errors.append(value);by_time[t].append(value)
 same(r['loss'],math.fsum(errors)/len(errors));same(r['per_horizon'],[math.fsum(v)/len(v) for v in by_time]);unchanged(before,[p,y,mask])
def invalid(m):
 for p,y,mask in [(np.ones((1,1,1,1,1))*1.1,np.zeros((1,1,1,1,1)),b([[True]])),(np.full((1,1,1,1,1),np.nan),np.zeros((1,1,1,1,1)),b([[True]])),(np.zeros((1,1,1,1,2)),np.zeros((1,1,1,1,2)),b([[True]])),(np.zeros((1,1,1,1,1)),np.zeros((1,1,1,1,1)),i([[1]]))]:reject(lambda:m.masked_video_loss(p,y,mask))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
