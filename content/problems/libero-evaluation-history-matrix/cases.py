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

def event(key,stage,task,success):return dict(evaluation_id=key,stage=stage,task_id=task,success=success)
def example1(m):
 e=event('e2',1,'a',True);r=m.continual_evaluation_matrix(['a','b'],[event('e1',0,'b',False),e,e.copy()]);same(r['counts'],[[0,1],[1,0],[0,0]]);same(r['successes'],[[0,0],[1,0],[0,0]]);same(r['rates'],[[np.nan,0],[1,np.nan],[np.nan,np.nan]])
def example2(m):
 r=m.continual_evaluation_matrix(['a'],[event('e1',1,'a',True),event('e2',1,'a',False)]);same(r['counts'],[[0],[2]]);same(r['successes'],[[0],[1]]);same(r['rates'],[[np.nan],[.5]])
def edges(m):
 r=m.continual_evaluation_matrix(['b','a'],[]);assert r['counts'].shape==(3,2) and np.isnan(r['rates']).all();assert r['counts'].dtype==np.int64
 r=m.continual_evaluation_matrix(['b','a'],[event('e',0,'a',True)]);assert r['counts'][0,1]==1
def oracle_scale(m):
 tasks=['t'+str(j) for j in range(32)];events=[event('e'+str(j),j%33,tasks[(j//33)%32],j%3==0) for j in range(50000)];before=copy.deepcopy(events);r=m.continual_evaluation_matrix(tasks,events+events);counts=np.zeros((33,32),dtype=np.int64);success=np.zeros_like(counts)
 for e in events:col=tasks.index(e['task_id']);counts[e['stage'],col]+=1;success[e['stage'],col]+=e['success']
 np.testing.assert_array_equal(r['counts'],counts);np.testing.assert_array_equal(r['successes'],success)
 expected_rates=np.array([[int(success[a,j])/int(counts[a,j]) if counts[a,j] else np.nan for j in range(32)] for a in range(33)]);same(r['rates'],expected_rates);assert events==before
def invalid(m):
 for order,events in [(['a','a'],[]),(['a'],[event('e',2,'a',True)]),(['a'],[event('e',0,'b',True)]),(['a'],[event('e',0,'a',1)]),(['a'],[event('e',0,'a',True),event('e',0,'a',False)]),(['a'],[event('e',0,'a',True),event('e',1,'a',True)])]:reject(lambda:m.continual_evaluation_matrix(order,events))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
