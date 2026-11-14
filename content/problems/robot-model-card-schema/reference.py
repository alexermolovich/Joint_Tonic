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

def _ids(v,lo=0,hi=128):
    _list(v,lo,hi)
    for item in v:_id(item)
    if len(set(v))!=len(v):raise ValueError('duplicate identifier')
    return v

def validate_robot_model_card(card, required_slices):
    _fields(card,'model_id artifacts intended_embodiments limitations metrics');_id(card['model_id']);_fields(card['artifacts'],'weights preprocessing action_decoder runtime')
    for value in card['artifacts'].values():_hash(value)
    _ids(card['intended_embodiments'],1);_ids(required_slices,0,256)
    if type(card['limitations']) is not str or not 1<=len(card['limitations'].strip())<=4096:raise ValueError('limitations')
    _list(card['metrics'],0,10000);seen=set();issues=[]
    for row in card['metrics']:
        _fields(row,'slice_id trials successes');key=_id(row['slice_id']);n=_int(row['trials'],0,10**9);k=_int(row['successes'],0,10**9)
        if key in seen:raise ValueError('duplicate slice')
        seen.add(key)
        if n==0:issues.append((key,'no_trials'))
        if k>n:issues.append((key,'invalid_success_count'))
    for key in set(required_slices)-seen:issues.append((key,'missing'))
    return sorted(issues)
