import math

import re

import numpy as np

def _id(x):
    if type(x) is not str or re.fullmatch(r'[a-z][a-z0-9_-]{0,31}',x) is None:
        raise ValueError('Invalid identifier')
    return x

def _integer(x,lo,hi):
    if type(x) is not int or not lo<=x<=hi:raise ValueError('Invalid integer')
    return x

def _record(x,keys):
    if type(x) is not dict or x.keys()!=set(keys):raise ValueError('Invalid record fields')

def _id_list(x,lo,hi):
    if type(x) is not list or not lo<=len(x)<=hi:raise ValueError('Invalid ID list')
    for v in x:_id(v)
    if len(set(x))!=len(x):raise ValueError('Duplicate ID')
    return x

def continual_evaluation_matrix(task_order, events):
    _id_list(task_order,1,256)
    if type(events) is not list or len(events)>100000:raise ValueError('Invalid events')
    lookup={key:j for j,key in enumerate(task_order)};seen={};k=len(task_order)
    counts=np.zeros((k+1,k),dtype=np.int64);successes=np.zeros_like(counts)
    for event in events:
        _record(event,['evaluation_id','stage','task_id','success'])
        key=_id(event['evaluation_id']);task=_id(event['task_id']);stage=_integer(event['stage'],0,k)
        if task not in lookup or type(event['success']) is not bool:raise ValueError('Invalid trial evidence')
        identity=(stage,task,event['success'])
        if key in seen:
            if seen[key]!=identity:raise ValueError('Conflicting retry')
            continue
        seen[key]=identity;col=lookup[task];counts[stage,col]+=1;successes[stage,col]+=int(event['success'])
    rates=np.full(counts.shape,np.nan,dtype=np.float64);np.divide(successes,counts,out=rates,where=counts>0)
    return dict(counts=counts,successes=successes,rates=rates)
