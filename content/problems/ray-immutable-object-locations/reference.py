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

def track_artifact_locations(events):
    _list(events,0,50000);objects={};all_nodes=set()
    for row in events:
        if type(row) is not dict or row.get('op') not in ('put','evict'):raise ValueError('event')
        put=row['op']=='put';_fields(row,'op artifact_id node_id sha256 size_bytes' if put else 'op artifact_id node_id')
        key=_id(row['artifact_id']);node=_id(row['node_id']);all_nodes.add(node)
        if len(all_nodes)>10000:raise ValueError('node budget')
        if put:
            digest=_hash(row['sha256']);size=_int(row['size_bytes'],0,10**12)
            if key not in objects:
                objects[key]=[digest,size,set()]
                if len(objects)>10000:raise ValueError('artifact budget')
            elif objects[key][:2]!=[digest,size]:raise ValueError('immutable identity')
            objects[key][2].add(node)
        else:
            if key not in objects:raise ValueError('unknown artifact')
            objects[key][2].discard(node)
    rows=[dict(artifact_id=k,sha256=v[0],size_bytes=v[1],nodes=sorted(v[2]),lost=not v[2]) for k,v in sorted(objects.items())]
    return dict(artifacts=rows,physical_bytes=sum(v[1]*len(v[2]) for v in objects.values()))
