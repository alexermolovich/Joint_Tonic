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

def task(key,demos,seeds):return dict(task_id=key,demo_ids=demos,evaluation_seed_ids=seeds)
def example1(m):
 r=m.continual_task_schedule([task('a',[3,1],[8]),task('b',[9],[2,1])],['b','a'],1)
 assert r==[dict(stage=1,task_id='b',selected_demo_ids=[9],evaluation_seed_ids=[1,2],cumulative_demo_count=1),dict(stage=2,task_id='a',selected_demo_ids=[1],evaluation_seed_ids=[8],cumulative_demo_count=2)]
def example2(m):assert m.continual_task_schedule([task('a',[5,2],[0])],['a'],10)==[dict(stage=1,task_id='a',selected_demo_ids=[2,5],evaluation_seed_ids=[0],cumulative_demo_count=2)]
def edges(m):
 hi=2**63-1;rows=[task('a',[hi],[hi]),task('b',[hi-1],[hi])];before=copy.deepcopy(rows);r=m.continual_task_schedule(rows,['a','b'],1);assert r[1]['cumulative_demo_count']==2 and r[0]['selected_demo_ids']==[hi];assert rows==before
 r[0]['selected_demo_ids'].append(0);assert rows==before
def oracle_scale(m):
 tasks=[task('t'+str(j),list(range(j*400,(j+1)*400))[::-1],[j+1,j]) for j in range(250)];order=[x['task_id'] for x in tasks][::-1];r=m.continual_task_schedule(tasks,order,17)
 for k,row in enumerate(r):
  j=249-k;assert row['selected_demo_ids']==list(range(j*400,j*400+17));assert row['evaluation_seed_ids']==[j,j+1];assert row['cumulative_demo_count']==(k+1)*17
def invalid(m):
 for tasks,order,budget in [([],[],1),([task('a',[1],[0])],['b'],1),([task('a',[1],[0]),task('b',[1],[1])],['a','b'],1),([task('a',[1,1],[0])],['a'],1),([task('a',[True],[0])],['a'],1),([task('a',[1],[0])],['a'],True),([task('a',[1],[])],['a'],1),([task('a',[1],[0])],['a','a'],1)]:reject(lambda:m.continual_task_schedule(tasks,order,budget))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
