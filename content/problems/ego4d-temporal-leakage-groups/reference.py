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

def temporal_split_groups(clips, heldout_ids, guard_ns):
    if type(clips) is not list or len(clips)>100000:raise ValueError('Invalid clips')
    _id_list(heldout_ids,0,100000);_integer(guard_ns,0,2**63-1)
    by_video={};seen=set()
    for clip in clips:
        _record(clip,['clip_id','video_id','start_ns','end_ns']);key=_id(clip['clip_id']);video=_id(clip['video_id'])
        start=_integer(clip['start_ns'],0,2**63-1);end=_integer(clip['end_ns'],0,2**63-1)
        if key in seen or start>=end:raise ValueError('Invalid clip identity/interval')
        seen.add(key);by_video.setdefault(video,[]).append((start,end,key))
    held=set(heldout_ids)
    if not held<=seen:raise ValueError('Unknown heldout clip')
    output=[]
    def emit(group):
        group_id=min(group);split='test' if held.intersection(group) else 'train'
        output.extend(dict(clip_id=key,group_id=group_id,split=split) for key in group)
    for intervals in by_video.values():
        group=[];right=None
        for start,end,key in sorted(intervals):
            if right is not None and start-right>guard_ns:emit(group);group=[];right=None
            group.append(key);right=end if right is None else max(right,end)
        if group:emit(group)
    return sorted(output,key=lambda r:r['clip_id'])
