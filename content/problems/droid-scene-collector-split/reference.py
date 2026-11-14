import re

_ID=re.compile(r'[a-z][a-z0-9_-]{0,31}\Z')

def _id(v):
    if type(v) is not str or _ID.fullmatch(v) is None:raise ValueError('identifier')
    return v

def _fields(v,fields):
    if type(v) is not dict or set(v)!=set(fields.split()):raise ValueError('fields')

def _list(v,lo=0,hi=10000):
    if type(v) is not list or not lo<=len(v)<=hi:raise ValueError('list')

def _ids(v,lo=0,hi=128):
    _list(v,lo,hi)
    for item in v:_id(item)
    if len(set(v))!=len(v):raise ValueError('duplicate identifier')
    return v

def split_scene_collector_components(episodes, held_out_scenes):
    _list(episodes,0,10000);_ids(held_out_scenes,0,10000);ids=set();scenes=set()
    for row in episodes:
        _fields(row,'episode_id scene_id collector_id')
        for value in row.values():_id(value)
        if row['episode_id'] in ids:raise ValueError('episode duplicate')
        ids.add(row['episode_id']);scenes.add(row['scene_id'])
    if not set(held_out_scenes)<=scenes:raise ValueError('unknown held-out scene')
    parent=list(range(len(episodes)));size=[1]*len(episodes);first={}
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):
        a,b=find(i),find(j)
        if a==b:return
        if size[a]<size[b]:a,b=b,a
        parent[b]=a;size[a]+=size[b]
    for i,row in enumerate(episodes):
        for field in ('scene_id','collector_id'):
            key=(field,row[field])
            if key in first:union(i,first[key])
            else:first[key]=i
    groups={}
    for i,row in enumerate(episodes):groups.setdefault(find(i),[]).append(row)
    held=set(held_out_scenes);train=[];test=[];labels={}
    for group in groups.values():
        names=sorted(row['episode_id'] for row in group);target=test if any(row['scene_id'] in held for row in group) else train;target.extend(names)
        for name in names:labels[name]=names[0]
    return dict(train_ids=sorted(train),test_ids=sorted(test),component_ids=dict(sorted(labels.items())))
