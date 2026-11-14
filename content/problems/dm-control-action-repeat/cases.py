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

def run(m,r,d,last,repeat):return m.aggregate_action_repeat(f(r),f(d),b(last),repeat)
def example1(m):assert run(m,[1,2,99],[.5,1,1],[False,True,False],3)==dict(reward=2.,discount=.5,steps=2,last=True)
def example2(m):assert run(m,[3,8],[0,1],[False,False],2)==dict(reward=3.,discount=0.,steps=2,last=False)
def edges(m):
 assert run(m,[4,100],[1,0],[True,False],2)==dict(reward=4.,discount=1.,steps=1,last=True)
 assert run(m,[-2,10],[.5,.5],[False,False],1)==dict(reward=-2.,discount=.5,steps=1,last=False)
 r=m.aggregate_action_repeat(np.ones(1,dtype=np.float32),np.zeros(1,dtype=np.float32),b([True]),1);assert type(r['reward']) is float and type(r['steps']) is int and type(r['last']) is bool
def oracle_scale(m):
 n=100000;r=np.tile(f([1,-1]),n)[::2];d=np.ones(n,dtype=np.float32);last=np.zeros(n,dtype=bool);before=[x.copy() for x in [r,d,last]]
 result=m.aggregate_action_repeat(r,d,last,n);assert result==dict(reward=100000.,discount=1.,steps=n,last=False);unchanged(before,[r,d,last])
 rng=np.random.default_rng(923)
 for _ in range(20):
  r=rng.normal(size=25);d=rng.uniform(size=25);last=np.zeros(25,dtype=bool);stop=int(rng.integers(0,25));last[stop]=True;limit=int(rng.integers(1,26));k=min(stop+1,limit)
  out=m.aggregate_action_repeat(r,d,last,limit);same(out['reward'],math.fsum(float(r[j])*math.prod(map(float,d[:j])) for j in range(k)));same(out['discount'],math.prod(map(float,d[:k])));assert out['steps']==k
def invalid(m):
 for r,d,last,n in [([],[],[],1),([1],[1],[False],0),([1],[1],[False],True),([1],[1],[False],2),([1],[1.1],[False],1),([1],[float('nan')],[False],1),([1,np.nan],[0,1],[True,False],1),([1],[1],[],1)]:reject(lambda:run(m,r,d,last,n))
 reject(lambda:m.aggregate_action_repeat(f([1]),f([1]),i([0]),1))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
