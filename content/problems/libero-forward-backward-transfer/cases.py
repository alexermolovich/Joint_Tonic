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
 r=m.continual_transfer_report(f([[.1,.2],[.8,.4],[.6,.9]]),np.ones((3,2),dtype=bool));same(r['forward'],[np.nan,.2]);same(r['backward'],[-.2,np.nan]);same(r['forgetting'],[.2,np.nan]);same([r['forward_mean'],r['backward_mean'],r['forgetting_mean'],r['final_mean']],[.2,-.2,.2,.75])
def example2(m):
 r=m.continual_transfer_report(f([[0],[1]]),np.ones((2,1),dtype=bool));assert r['final_mean']==1 and all(math.isnan(r[key]) for key in ['forward_mean','backward_mean','forgetting_mean'])
def edges(m):
 x=f([[np.inf,np.nan],[.2,.3],[.8,np.nan]]);mask=b([[False,False],[True,True],[True,False]]);r=m.continual_transfer_report(x,mask);same(r['backward'],[.6,np.nan]);same(r['forgetting'],[0,np.nan]);assert math.isnan(r['forward_mean']) and r['final_mean']==.8
 x=np.full((4,3),.5);mask=np.ones_like(x,dtype=bool);mask[2,0]=False;x[2,0]=np.nan;r=m.continual_transfer_report(x,mask);assert r['backward'][0]==0 and math.isnan(r['forgetting'][0])
def oracle_scale(m):
 rng=np.random.default_rng(933);raw=rng.uniform(size=(257,512));x=raw[:,::2];mask=rng.uniform(size=x.shape)>.1;before=[x.copy(),mask.copy()];r=m.continual_transfer_report(x,mask);k=256
 for j in range(k):
  forward=x[j,j]-x[0,j] if j>=1 and mask[j,j] and mask[0,j] else np.nan
  backward=x[k,j]-x[j+1,j] if j<k-1 and mask[k,j] and mask[j+1,j] else np.nan
  forgetting=max(float(x[a,j]) for a in range(j+1,k+1))-x[k,j] if j<k-1 and all(mask[a,j] for a in range(j+1,k+1)) else np.nan
  same([r['forward'][j],r['backward'][j],r['forgetting'][j]],[forward,backward,forgetting])
 unchanged(before,[x,mask])
def invalid(m):
 for x,mask in [(f([[0],[1.1]]),b([[True],[True]])),(f([[0],[np.nan]]),b([[True],[True]])),(np.zeros((2,2)),np.ones((2,2),dtype=bool)),(np.zeros((2,1)),i([[1],[1]])),(np.zeros((2,1)),b([[True]]))]:reject(lambda:m.continual_transfer_report(x,mask))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
