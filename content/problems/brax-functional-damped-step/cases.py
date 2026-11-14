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
 r=m.functional_damped_step(f([[0]]),f([[1]]),f([[3]]),f([2]),f([1]),.1);same(r['velocity'],[[1.1]]);same(r['position'],[[.11]])
def example2(m):
 r=m.functional_damped_step(f([[2]]),f([[0]]),f([[0]]),f([1]),f([0]),.1);same(r['velocity'],[[0]]);same(r['position'],[[2]])
def edges(m):
 r=m.functional_damped_step(np.zeros((0,2)),np.zeros((0,2)),np.zeros((0,2)),f([1,2]),f([0,1]),.1);assert r['position'].shape==(0,2)
 r=m.functional_damped_step(np.ones((1,2),dtype=np.float32),np.zeros((1,2),dtype=np.float32),f([[1,2]]),f([1,2]),f([0,0]),.1);same(r['position'],[[1.01,1.01]]);same(r['velocity'],[[.1,.1]]);assert r['position'].dtype==np.float64
def oracle_scale(m):
 rng=np.random.default_rng(929);q=rng.normal(size=(3000,64))[:,::2];v=rng.normal(size=q.shape);force=rng.normal(size=q.shape);mass=np.linspace(.1,10,32);damping=np.linspace(0,2,32);args=[q,v,force,mass,damping];before=[x.copy() for x in args];h=.01;r=m.functional_damped_step(*args,h)
 expected_v=np.array([[float(v[a,c])+h*(float(force[a,c])-float(damping[c])*float(v[a,c]))/float(mass[c]) for c in range(32)] for a in range(len(q))]);same(r['velocity'],expected_v);same(r['position'],q+h*expected_v);unchanged(before,args);assert all(not np.shares_memory(out,x) for out in r.values() for x in args)
def invalid(m):
 base=[f([[0]]),f([[1]]),f([[3]]),f([2]),f([1]),.1]
 for index,value in [(0,f([[1e4+1]])),(1,f([[np.nan]])),(2,i([[1]])),(3,f([0])),(3,f([1001])),(4,f([-1])),(4,f([1001])),(5,0),(5,True),(5,np.float64(.1)),(5,10**1000)]:
  a=base.copy();a[index]=value;reject(lambda:m.functional_damped_step(*a))
 reject(lambda:m.functional_damped_step(np.zeros((0,1)),np.zeros((0,1)),np.zeros((0,1)),f([0]),f([0]),.1))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
