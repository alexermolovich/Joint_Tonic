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

def run(m,ids):return m.video_transition_windows(f([0,.2,.4]).reshape(3,1,1,1),f([[1],[2]]),b([True]*3),i(ids),i([0]),3)
def example1(m):
 r=run(m,[0,0,0]);same(r['current'].ravel(),[0,.2,0]);same(r['next'].ravel(),[.2,.4,0]);same(r['actions'].ravel(),[1,2,0]);np.testing.assert_array_equal(r['valid'],[[True,True,False]])
def example2(m):r=run(m,[0,1,1]);assert not r['valid'].any() and not r['actions'].any() and not r['next'].any()
def edges(m):
 r=m.video_transition_windows(np.zeros((1,1,1,3),dtype=np.float32),np.zeros((0,2)),b([True]),i([0]),i([0]),2);assert r['current'].shape==(1,2,1,1,3) and not r['valid'].any()
 r=m.video_transition_windows(np.zeros((2,1,1,1)),np.zeros((1,2)),b([False,True]),i([0,0]),i([]),1);assert r['actions'].shape==(0,1,2)
def oracle_scale(m):
 t=1000;x=(np.arange(t*2,dtype=np.float64)[::2]/(2*t)).reshape(t,1,1,1);a=np.arange((t-1)*4,dtype=np.float64).reshape(t-1,4)[:,::2];obs=np.arange(t)%7!=0;ids=np.arange(t,dtype=np.int64)//100;starts=np.arange(0,t,3,dtype=np.int64);args=[x,a,obs,ids,starts];before=[v.copy() for v in args];r=m.video_transition_windows(*args,8)
 for row,start in enumerate(starts):
  for k in range(8):
   j=int(start)+k;valid=j+1<t and obs[j] and obs[j+1] and ids[j]==ids[j+1]==ids[start];assert r['valid'][row,k]==valid
   same(r['current'][row,k],x[j] if valid else np.zeros((1,1,1)));same(r['next'][row,k],x[j+1] if valid else np.zeros((1,1,1)));same(r['actions'][row,k],a[j] if valid else np.zeros(2))
 unchanged(before,args)
def invalid(m):
 base=[np.zeros((4,1,1,1)),np.zeros((3,1)),b([True]*4),i([0]*4),i([0]),2]
 for pos,value in [(0,np.full((4,1,1,1),np.nan)),(1,np.full((3,1),np.inf)),(3,i([0,1,0,0])),(4,i([-1])),(4,i([4])),(5,True)]:
  a=base.copy();a[pos]=value;reject(lambda:m.video_transition_windows(*a))
 reject(lambda:m.video_transition_windows(np.zeros((2,1,1,1)),np.zeros((1,32)),b([True,True]),i([0,0]),np.zeros(4096,dtype=np.int64),8))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
