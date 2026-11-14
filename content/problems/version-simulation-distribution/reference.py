import math
import json
import re
import hashlib

def version_scenario_distribution(config):
    def name(x):return type(x) is str and re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',x) is not None
    if type(config) is not dict or set(config)!={'simulator','asset_sha256','seed','reset','factors'}:raise ValueError('configuration schema')
    sim=config['simulator'];digest=config['asset_sha256'];seed=config['seed'];reset=config['reset'];factors=config['factors']
    if type(sim) is not str or re.fullmatch(r'[a-z][a-z0-9_.-]{0,63}',sim) is None or type(digest) is not str or re.fullmatch('[0-9a-f]{64}',digest) is None:raise ValueError('runtime identity')
    if type(seed) is not int or not 0<=seed<=2**32-1 or type(reset) is not str or reset!='episode' or type(factors) is not list or not 1<=len(factors)<=32:raise ValueError('sampling policy')
    seen=set();normalized=[]
    for factor in factors:
        if type(factor) is not dict or set(factor)!={'name','unit','low','high'}:raise ValueError('factor schema')
        key,unit,low,high=(factor[k] for k in ['name','unit','low','high'])
        if not name(key) or key in seen or type(unit) is not str or unit not in ('kg','rad','s','ratio'):raise ValueError('factor identity')
        if any(type(v) not in (int,float) or not -1e6<=v<=1e6 or not math.isfinite(v) for v in [low,high]) or low>high:raise ValueError('interval')
        if (unit=='kg' and low<=0) or (unit in ('s','ratio') and low<0) or (unit=='rad' and (low<-math.pi or high>math.pi)):raise ValueError('physical interval')
        seen.add(key);normalized.append(dict(name=key,unit=unit,low=0.0 if low==0 else float(low),high=0.0 if high==0 else float(high)))
    out=dict(simulator=sim,asset_sha256=digest,seed=seed,reset=reset,factors=sorted(normalized,key=lambda f:f['name']))
    payload=json.dumps(out,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('utf-8')
    return dict(config=out,sha256=hashlib.sha256(payload).hexdigest())
