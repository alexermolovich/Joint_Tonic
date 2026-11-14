"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):np.testing.assert_array_equal(a,b)

def run(m,t,a,observed=None,limit=None,dead=.1,samples=2,duration=0):
 a=np.array(a,dtype=np.float64);observed=np.ones(a.shape[0],dtype=bool) if observed is None else np.array(observed,dtype=bool);limit=np.full(a.shape[1],2.) if limit is None else np.array(limit,dtype=np.float64)
 return m.action_segment_report(np.array(t,dtype=np.int64),a,observed,limit,dead,samples,duration)
def example1(m):
 r=run(m,[0,10,20,30],[[0],[0],[1],[0]],duration=10);same(r['corrupt'],[False]*4);same(r['paused'],[True,True,False,False]);assert r['segments']==[(0,2,10)]
def example2(m):
 r=run(m,[0,10,20],[[0],[np.nan],[0]]);same(r['corrupt'],[False,True,False]);same(r['paused'],[False]*3);assert r['segments']==[]
def edges(m):
 high=2**63-1;r=run(m,[high-2,high-1,high],[[0],[0],[0]],duration=2);assert r['segments']==[(0,3,2)] and r['paused'].all()
 r=run(m,[0],[[0]],samples=1,duration=0);assert r['segments']==[(0,1,0)]
 r=run(m,[0,1,2,3],[[2],[-2],[np.inf],[0]],observed=[True,True,True,False]);same(r['corrupt'],[False,False,True,True]);assert not r['paused'].any()
 r=m.action_segment_report(np.zeros(0,dtype=np.int64),np.empty((0,2)),np.zeros(0,dtype=bool),np.ones(2),0.,1,0);assert r['segments']==[] and r['paused'].shape==(0,)
 r=run(m,[0,1],[[1e308],[-1e308]]);assert r['corrupt'].all()
def oracle_scale(m):
 t=np.arange(200000,dtype=np.int64)[::2];a=np.zeros((200000,2),dtype=np.float32)[::2];observed=np.ones(100000,dtype=bool);a[::11,0]=1;observed[::17]=False;before=[t.copy(),a.copy(),observed.copy()];r=m.action_segment_report(t,a,observed,np.ones(2),.1,3,4)
 corrupt=[not bool(observed[i]) for i in range(100000)];candidate=[not corrupt[i] and i%11!=0 for i in range(100000)];segments=[];paused=np.zeros(100000,dtype=bool);i=0
 while i<100000:
  if not candidate[i]:i+=1;continue
  j=i+1
  while j<100000 and candidate[j]:j+=1
  if j-i>=3 and 2*(j-i-1)>=4:segments.append((i,j,2*(j-i-1)));paused[i:j]=True
  i=j
 same(r['corrupt'],corrupt);same(r['paused'],paused);assert r['segments']==segments
 for x,y in zip(before,[t,a,observed]):np.testing.assert_array_equal(x,y)
 assert r['corrupt'].dtype==r['paused'].dtype==np.bool_ and all(type(v) is int for row in segments for v in row)
def invalid(m):
 for t,a in [([1,1],[[0],[0]]),([-1],[[0]])]:reject(lambda:run(m,t,a))
 reject(lambda:run(m,[0],[[0]],samples=0));reject(lambda:run(m,[0],[[0]],duration=-1));reject(lambda:run(m,[0],[[0]],dead=3));reject(lambda:run(m,[0],[[0]],limit=[0]))
 reject(lambda:m.action_segment_report(np.array([0],dtype=np.int64),np.array([[0]],dtype=np.int64),np.array([True]),np.array([1.]),0.,1,0))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
