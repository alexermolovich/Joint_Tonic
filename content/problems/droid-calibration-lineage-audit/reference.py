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

def audit_calibration_lineage(episodes, calibrations):
    _list(episodes,0,10000);_list(calibrations,0,10000);lookup={};seen=set()
    for c in calibrations:
        _fields(c,'calibration_id session_id robot_id sha256 valid_from_ns valid_until_ns')
        for field in ('calibration_id','session_id','robot_id'):_id(c[field])
        _hash(c['sha256']);_int(c['valid_from_ns']);_int(c['valid_until_ns'])
        if c['calibration_id'] in lookup or c['valid_from_ns']>=c['valid_until_ns']:raise ValueError('calibration interval/identity')
        lookup[c['calibration_id']]=c
    issues=[]
    for e in episodes:
        _fields(e,'episode_id session_id robot_id calibration_id calibration_sha256 start_ns end_ns')
        for field in ('episode_id','session_id','robot_id','calibration_id'):_id(e[field])
        _hash(e['calibration_sha256']);_int(e['start_ns']);_int(e['end_ns']);key=e['episode_id']
        if key in seen or e['start_ns']>=e['end_ns']:raise ValueError('episode interval/identity')
        seen.add(key);c=lookup.get(e['calibration_id'])
        if c is None:issues.append((key,'unknown_calibration'));continue
        for field,code in [('session_id','session_mismatch'),('robot_id','robot_mismatch')]:
            if e[field]!=c[field]:issues.append((key,code))
        if e['calibration_sha256']!=c['sha256']:issues.append((key,'digest_mismatch'))
        if e['start_ns']<c['valid_from_ns'] or e['end_ns']>c['valid_until_ns']:issues.append((key,'validity_gap'))
    return sorted(issues)
