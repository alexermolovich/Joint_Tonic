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

def data_use_review_flags(datasets, requested_use, requested_embodiment):
    _list(datasets,0,10000);_id(requested_use);_id(requested_embodiment);seen=set();rows=[]
    for d in datasets:
        _fields(d,'dataset_id intended_uses prohibited_uses embodiments contains_personal_data consent license_known');key=_id(d['dataset_id'])
        if key in seen:raise ValueError('duplicate dataset')
        seen.add(key)
        for field in ('intended_uses','prohibited_uses','embodiments'):_ids(d[field])
        if type(d['contains_personal_data']) is not bool or type(d['license_known']) is not bool or type(d['consent']) is not str or d['consent'] not in ('granted','denied','unknown'):raise ValueError('declared status')
        flags=[]
        if requested_use in d['prohibited_uses']:flags.append('prohibited_use')
        if requested_use not in d['intended_uses']:flags.append('outside_intended_use')
        if requested_embodiment not in d['embodiments']:flags.append('unsupported_embodiment')
        if not d['license_known']:flags.append('unknown_license')
        if d['contains_personal_data'] and d['consent']!='granted':flags.append('consent_'+d['consent'])
        rows.append(dict(dataset_id=key,flags=sorted(flags),needs_review=bool(flags)))
    return sorted(rows,key=lambda row:row['dataset_id'])
