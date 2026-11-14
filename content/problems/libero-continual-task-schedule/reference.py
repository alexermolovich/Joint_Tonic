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

def continual_task_schedule(tasks, order, budget):
    if type(tasks) is not list or not 1<=len(tasks)<=256:raise ValueError('Invalid tasks')
    _id_list(order,1,256);_integer(budget,1,10000)
    table={};all_demos=set();demo_count=0;seed_count=0
    for task in tasks:
        _record(task,['task_id','demo_ids','evaluation_seed_ids']);key=_id(task['task_id'])
        if key in table:raise ValueError('Duplicate task')
        for field in ['demo_ids','evaluation_seed_ids']:
            values=task[field]
            if type(values) is not list or not 1<=len(values)<=10000:raise ValueError('Invalid identity list')
            for value in values:_integer(value,0,2**63-1)
            if len(set(values))!=len(values):raise ValueError('Duplicate identity')
        if all_demos.intersection(task['demo_ids']):raise ValueError('Demonstration assigned twice')
        all_demos.update(task['demo_ids']);demo_count+=len(task['demo_ids']);seed_count+=len(task['evaluation_seed_ids']);table[key]=task
    if demo_count>100000 or seed_count>100000 or set(order)!=set(table):raise ValueError('Invalid schedule coverage or size')
    rows=[];total=0
    for stage,key in enumerate(order,1):
        task=table[key];selected=sorted(task['demo_ids'])[:budget];total+=len(selected)
        rows.append(dict(stage=stage,task_id=key,selected_demo_ids=selected,evaluation_seed_ids=sorted(task['evaluation_seed_ids']),cumulative_demo_count=total))
    return rows
