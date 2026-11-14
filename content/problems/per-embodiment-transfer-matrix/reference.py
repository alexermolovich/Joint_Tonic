import re
import numpy as np

def build_transfer_matrix(sources, targets, records):
    def axis(values):
        if type(values) is not list or not 1<=len(values)<=128 or any(type(v) is not str or re.fullmatch(r"[a-z][a-z0-9_-]{0,63}",v) is None for v in values) or len(set(values))!=len(values):
            raise ValueError("unique bounded axis IDs required")
    axis(sources);axis(targets)
    if type(records) is not list or len(records)>100000:raise ValueError("records list")
    rows={v:i for i,v in enumerate(sources)};cols={v:i for i,v in enumerate(targets)}
    successes=np.zeros((len(sources),len(targets)),dtype=np.int64);trials=np.zeros_like(successes)
    for record in records:
        if type(record) is not tuple or len(record)!=4:raise ValueError("record tuple")
        source,target,s,n=record
        if type(source) is not str or type(target) is not str or source not in rows or target not in cols:raise ValueError("unknown axis ID")
        if type(s) is not int or type(n) is not int or not 1<=n<=1000000 or not 0<=s<=n:raise ValueError("trial counts")
        successes[rows[source],cols[target]]+=s;trials[rows[source],cols[target]]+=n
    observed=trials>0;rates=np.full(successes.shape,np.nan,dtype=np.float64)
    np.divide(successes,trials,out=rates,where=observed)
    return dict(successes=successes,trials=trials,observed=observed,rates=rates)
