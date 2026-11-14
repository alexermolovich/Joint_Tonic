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

def run(m,t,s,r):return m.seeded_return_summary(i(t),i(s),f(r))
def example1(m):
 r=run(m,[0,0,0,1],[1,1,2,1],[0,2,9,4]);same(r['task_ids'],[0,1]);same(r['seeds'],[1,2]);same(r['counts'],[[2,1],[1,0]]);same(r['means'],[[1,9],[4,np.nan]]);same(r['task_means'],[5,4]);assert r['overall']==4.5
def example2(m):
 r=run(m,[2,2],[7,7],[-1,1]);same(r['counts'],[[2]]);same(r['means'],[[0]]);same(r['task_means'],[0]);assert r['overall']==0
def edges(m):
 r=run(m,[],[],[]);assert r['means'].shape==(0,0) and r['task_means'].shape==(0,) and math.isnan(r['overall']);assert r['counts'].dtype==np.int64
 hi=np.iinfo(np.int64).max;r=run(m,[hi,hi-1],[hi,hi-1],[2,6]);np.testing.assert_array_equal(r['task_ids'],[hi-1,hi]);same(r['task_means'],[6,2]);assert r['overall']==4
def oracle_scale(m):
 rng=np.random.default_rng(925);t=rng.integers(0,50,size=80000,dtype=np.int64)[::2];s=rng.integers(0,20,size=80000,dtype=np.int64)[::2];v=rng.integers(-100,100,size=80000).astype(np.float32)[::2];before=[x.copy() for x in [t,s,v]]
 cells={}
 for task,seed,value in zip(t,s,v):cells.setdefault((int(task),int(seed)),[]).append(float(value))
 expected=np.array([[math.fsum(cells[(task,seed)])/len(cells[(task,seed)]) if (task,seed) in cells else np.nan for seed in sorted(set(s.tolist()))] for task in sorted(set(t.tolist()))]);r=m.seeded_return_summary(t,s,v);same(r['means'],expected);same(r['task_means'],np.nanmean(expected,axis=1));same(r['overall'],np.mean(np.nanmean(expected,axis=1)));unchanged(before,[t,s,v])
 for value in r.values():
  if isinstance(value,np.ndarray):assert all(not np.shares_memory(value,x) for x in [t,s,v])
def invalid(m):
 for t,s,r in [([-1],[0],[1]),([0],[-1],[1]),([0],[],[1]),([0],[0],[np.nan])]:reject(lambda:run(m,t,s,r))
 reject(lambda:m.seeded_return_summary(f([0]),i([0]),f([1])))
 reject(lambda:m.seeded_return_summary(np.arange(1001,dtype=np.int64),np.arange(1001,dtype=np.int64),np.ones(1001)))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
