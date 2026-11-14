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
 r=m.activity_confusion_report(i([0,0,0]),i([0,0,1]),i([0,1,0]),b([True]*3),2);same(r['confusion'],[[[1,1],[1,0]]]);same(r['support'],[[2,1]]);same(r['recall'],[[.5,0]]);same(r['macro_recall'],[.25])
def example2(m):
 r=m.activity_confusion_report(i([2,2]),i([-1,1]),i([99,1]),b([False,True]),3);same(r['support'],[[0,1,0]]);same(r['recall'],[[np.nan,1,np.nan]]);same(r['macro_recall'],[1])
def edges(m):
 r=m.activity_confusion_report(i([5]),i([-1]),i([-1]),b([False]),1);same(r['dataset_ids'],[5]);assert np.isnan(r['macro_recall']).all() and not r['support'].any()
 r=m.activity_confusion_report(i([]),i([]),i([]),b([]),3);assert r['confusion'].shape==(0,3,3) and r['recall'].shape==(0,3)
 hi=2**63-1;r=m.activity_confusion_report(i([hi,hi-1]),i([0,0]),i([0,0]),b([True,True]),1);np.testing.assert_array_equal(r['dataset_ids'],[hi-1,hi])
def oracle_scale(m):
 rng=np.random.default_rng(939);ids=rng.integers(0,20,size=100000,dtype=np.int64)[::2];truth=rng.integers(0,8,size=100000,dtype=np.int64)[::2];pred=rng.integers(0,8,size=100000,dtype=np.int64)[::2];mask=np.arange(len(ids))%3!=0;before=[x.copy() for x in [ids,truth,pred,mask]];r=m.activity_confusion_report(ids,truth,pred,mask,8);expected=np.zeros((20,8,8),dtype=np.int64)
 for dataset,t,p,valid in zip(ids,truth,pred,mask):
  if valid:expected[dataset,t,p]+=1
 np.testing.assert_array_equal(r['confusion'],expected);same(r['support'],expected.sum(axis=2))
 recall=np.array([[int(expected[d,c,c])/sum(map(int,expected[d,c])) for c in range(8)] for d in range(20)]);same(r['recall'],recall);same(r['macro_recall'],[sum(map(float,row))/8 for row in recall]);unchanged(before,[ids,truth,pred,mask])
def invalid(m):
 for ids,t,p,mask,c in [(i([-1]),i([0]),i([0]),b([True]),1),(i([0]),i([-1]),i([0]),b([True]),1),(i([0]),i([0]),i([1]),b([True]),1),(i([0]),i([0]),i([0]),i([1]),1),(i([0]),i([0]),i([0]),b([True]),True)]:reject(lambda:m.activity_confusion_report(ids,t,p,mask,c))
 reject(lambda:m.activity_confusion_report(np.arange(245,dtype=np.int64),np.zeros(245,dtype=np.int64),np.zeros(245,dtype=np.int64),np.ones(245,dtype=bool),64))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
