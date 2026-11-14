import re

_ID=re.compile(r'[a-z][a-z0-9_-]{0,31}\Z')

_HASH=re.compile(r'[0-9a-f]{64}\Z')

def validate_robot_datasheet(document):
    if type(document) is not dict or len(document)>32 or any(type(k) is not str or not 1<=len(k)<=64 for k in document):raise ValueError('document')
    text={'dataset_id','version','motivation','collection_method','calibration_sha256','license','maintenance','limitations'}
    lists={'embodiments','sensors','tasks','intended_uses','prohibited_uses'};required=text|lists;issues=[]
    for key in required-set(document):issues.append((key,'missing'))
    for key in set(document)-required:issues.append((key,'unexpected'))
    for key in required&set(document):
        value=document[key];code=None
        if key in text:
            if type(value) is not str or not 1<=len(value.strip())<=1024:code='invalid'
            elif value=='unknown':code='unknown' if key in ('calibration_sha256','license') else 'invalid'
            elif key=='dataset_id' and not _ID.fullmatch(value):code='invalid'
            elif key=='calibration_sha256' and not _HASH.fullmatch(value):code='invalid'
            elif key=='version' and not re.fullmatch(r'(0|[1-9][0-9]{0,3})\.(0|[1-9][0-9]{0,3})\.(0|[1-9][0-9]{0,3})',value):code='invalid'
        else:
            low=0 if key=='prohibited_uses' else 1
            if type(value) is not list or not low<=len(value)<=128 or any(type(v) is not str or not _ID.fullmatch(v) for v in value) or len(set(value))!=len(value):code='invalid'
        if code:issues.append((key,code))
    return sorted(issues)
