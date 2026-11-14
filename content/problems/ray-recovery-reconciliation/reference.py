import re

_ID=re.compile(r'[a-z][a-z0-9_-]{0,31}\Z')

_HASH=re.compile(r'[0-9a-f]{64}\Z')

def _id(v):
    if type(v) is not str or _ID.fullmatch(v) is None:raise ValueError('identifier')
    return v

def _hash(v):
    if type(v) is not str or _HASH.fullmatch(v) is None:raise ValueError('digest')
    return v

def _int(v,lo=0,hi=2**63-1):
    if type(v) is not int or not lo<=v<=hi:raise ValueError('integer')
    return v

def _fields(v,fields):
    if type(v) is not dict or set(v)!=set(fields.split()):raise ValueError('fields')

def _list(v,lo=0,hi=10000):
    if type(v) is not list or not lo<=len(v)<=hi:raise ValueError('list')

def reconcile_task_attempts(tasks, events, max_attempts):
    _list(tasks,1,10000);_list(events,0,50000);_int(max_attempts,1,16)
    registry={};attempts={};successes={}
    for row in tasks:
        _fields(row,'task_id replay_safe');key=_id(row['task_id'])
        if key in registry or type(row['replay_safe']) is not bool:raise ValueError('task')
        registry[key]=row['replay_safe'];attempts[key]={};successes[key]=set()
    for row in events:
        _fields(row,'task_id attempt status digest');key=_id(row['task_id']);n=_int(row['attempt'],1,max_attempts);status=row['status'];digest=row['digest']
        if key not in registry or type(status) is not str or status not in ('failed','succeeded'):raise ValueError('event')
        if status=='succeeded':_hash(digest);successes[key].add(digest)
        elif digest is not None:raise ValueError('failed digest')
        evidence=(status,digest)
        if n in attempts[key] and attempts[key][n]!=evidence:raise ValueError('contradictory attempt')
        attempts[key][n]=evidence
        if len(successes[key])>1:raise ValueError('nonimmutable result')
    out=[]
    for key in sorted(registry):
        highest=max(attempts[key],default=0);digest=None;next_attempt=None
        if successes[key]:state='succeeded';digest=next(iter(successes[key]))
        elif highest==0:state='pending';next_attempt=1
        elif highest==max_attempts:state='exhausted'
        elif not registry[key]:state='blocked'
        else:state='retry';next_attempt=highest+1
        out.append(dict(task_id=key,state=state,next_attempt=next_attempt,digest=digest))
    return out
