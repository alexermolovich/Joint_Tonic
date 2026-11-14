"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):
    np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)

def event(task,attempt=1,status='failed',digest=None):return dict(task_id=task,attempt=attempt,status=status,digest=digest)
def example1(m):
 tasks=[dict(task_id='a',replay_safe=True),dict(task_id='b',replay_safe=False)]
 assert m.reconcile_task_attempts(tasks,[event('a')],3)==[dict(task_id='a',state='retry',next_attempt=2,digest=None),dict(task_id='b',state='pending',next_attempt=1,digest=None)]
def example2(m):
 tasks=[dict(task_id='a',replay_safe=True)];events=[event('a',1,'succeeded','1'*64),event('a',2)]
 wanted=[dict(task_id='a',state='succeeded',next_attempt=None,digest='1'*64)]
 assert m.reconcile_task_attempts(tasks,events,3)==wanted;assert m.reconcile_task_attempts(tasks,events[::-1]*2,3)==wanted

def edges(m):
 tasks=[dict(task_id='a',replay_safe=False),dict(task_id='b',replay_safe=False)]
 assert m.reconcile_task_attempts(tasks,[event('a',1),event('b',3)],3)==[dict(task_id='a',state='blocked',next_attempt=None,digest=None),dict(task_id='b',state='exhausted',next_attempt=None,digest=None)]
 r=m.reconcile_task_attempts([dict(task_id='a',replay_safe=True)],[event('a',1,'succeeded','1'*64),event('a',2,'succeeded','1'*64)],2);assert r[0]['state']=='succeeded'
def oracle_scale(m):
 tasks=[dict(task_id='t'+str(i),replay_safe=i%2==0) for i in range(5000)];events=[event(t['task_id']) for t in tasks];before=copy.deepcopy((tasks,events));result=m.reconcile_task_attempts(tasks[::-1],events[::-1]+events,3)
 expected=[dict(task_id=t['task_id'],state='retry' if t['replay_safe'] else 'blocked',next_attempt=2 if t['replay_safe'] else None,digest=None) for t in sorted(tasks,key=lambda t:t['task_id'])]
 assert result==expected and (tasks,events)==before

def invalid(m):
 t=[dict(task_id='a',replay_safe=True)]
 for ev in [[event('unknown')],[event('a',0)],[event('a',1),event('a',1,'succeeded','1'*64)],[event('a',1,'succeeded','1'*64),event('a',2,'succeeded','2'*64)],[event('a',1,'failed','1'*64)],[event('a',1,'succeeded','BAD')]]:reject(lambda:m.reconcile_task_attempts(t,ev,3))
 reject(lambda:m.reconcile_task_attempts(t+t,[],3));reject(lambda:m.reconcile_task_attempts([],[],3));reject(lambda:m.reconcile_task_attempts(t,[],True))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
