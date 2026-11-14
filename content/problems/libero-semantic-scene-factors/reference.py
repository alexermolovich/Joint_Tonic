import math

import re

import numpy as np

def _id(x):
    if type(x) is not str or re.fullmatch(r'[a-z][a-z0-9_-]{0,31}',x) is None:
        raise ValueError('Invalid identifier')
    return x

def _record(x,keys):
    if type(x) is not dict or x.keys()!=set(keys):raise ValueError('Invalid record fields')

def semantic_scene_groups(records):
    if type(records) is not list or len(records)>10000:raise ValueError('Invalid records')
    groups={};seen=set()
    for row in records:
        _record(row,['task_id','verb','object_id','goal_id','scene_id'])
        for value in row.values():_id(value)
        if row['task_id'] in seen:raise ValueError('Duplicate task')
        seen.add(row['task_id']);key=(row['verb'],row['object_id'],row['goal_id'])
        tasks,scenes=groups.setdefault(key,([],set()));tasks.append(row['task_id']);scenes.add(row['scene_id'])
    return [dict(semantic_key=key,task_ids=sorted(tasks),scene_ids=sorted(scenes),has_scene_variation=len(scenes)>1) for key,(tasks,scenes) in sorted(groups.items())]
