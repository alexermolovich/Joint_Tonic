import numpy as np

def _int(v,lo=0,hi=2**63-1):
    if type(v) is not int or not lo<=v<=hi:raise ValueError('integer')
    return v

def _ints(v,rank=1):
    if not isinstance(v,np.ndarray) or v.dtype!=np.int64 or v.ndim!=rank:raise ValueError('integer array')
    return v

def policy_staleness_report(current_version, sample_versions, sample_counts, max_lag):
    _int(current_version);_int(max_lag);v=_ints(sample_versions);n=_ints(sample_counts)
    if v.shape!=n.shape or v.size>100000 or np.any(v<0) or np.any(n<0) or np.any(n>10**6):raise ValueError('samples')
    lag=current_version-v;future=lag<0;stale=lag>max_lag;accepted=~future&~stale
    accepted_count=sum(int(x) for x in n[accepted]);rejected_count=sum(int(x) for x in n[~accepted]);known_count=sum(int(x) for x in n[~future])
    numerator=sum(int(a)*int(b) for a,b in zip(lag[~future],n[~future]))
    mean=numerator/known_count if known_count else float('nan')
    return dict(lag=lag,future=future,stale=stale,accepted=accepted,accepted_samples=accepted_count,rejected_samples=rejected_count,mean_known_lag=float(mean))
