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

def run(m,s,e,n,u,w):return m.simulation_throughput(i(s),i(e),i(n),i(u),w)
def example1(m):assert run(m,[0,2000000000],[1000000000,4000000000],[100,400],[1,6],1)==dict(duration_ns=2000000000,environment_steps=400,learner_updates=6,steps_per_second=200.,updates_per_second=3.)
def example2(m):
 r=run(m,[0,2000000000],[1000000000,4000000000],[100,400],[1,6],2);assert r['duration_ns']==r['environment_steps']==r['learner_updates']==0 and math.isnan(r['steps_per_second']) and math.isnan(r['updates_per_second'])
def edges(m):
 hi=np.iinfo(np.int64).max;r=run(m,[hi-10,hi-4],[hi-7,hi],[3,4],[0,1],0);assert r['duration_ns']==7 and r['steps_per_second']==1e9;same(r['updates_per_second'],1e9/7)
 r=run(m,[],[],[],[],0);assert math.isnan(r['steps_per_second'])
 r=run(m,[0,1],[1,2],[0,0],[0,0],0);assert r['steps_per_second']==0 and type(r['duration_ns']) is int
def oracle_scale(m):
 count=100000;s=np.arange(count*2,dtype=np.int64)[::2]*1000;e=s+1000;n=np.full(count,1000000000,dtype=np.int64);u=np.ones(count,dtype=np.int64);before=[x.copy() for x in [s,e,n,u]]
 r=m.simulation_throughput(s,e,n,u,123);retained=count-123;assert r['duration_ns']==retained*1000 and r['environment_steps']==retained*1000000000 and r['learner_updates']==retained;same(r['steps_per_second'],1e15);same(r['updates_per_second'],1e6);unchanged(before,[s,e,n,u])
def invalid(m):
 for s,e,n,u,w in [([0],[0],[1],[1],0),([0,1],[2,3],[1,1],[1,1],0),([-1],[1],[1],[1],0),([1,0],[2,1],[1,1],[1,1],0),([0],[1],[-1],[1],0),([0],[1],[1],[1000000001],0),([0],[1],[1],[1],True),([0],[1],[1],[1],2),([0],[1],[],[1],0)]:reject(lambda:run(m,s,e,n,u,w))
 reject(lambda:m.simulation_throughput(f([0]),i([1]),i([1]),i([1]),0))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
