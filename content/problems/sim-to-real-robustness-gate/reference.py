import math
import re

def robustness_release_gate(required, evidence, expected_distribution, min_trials, min_success_rate, min_worst_return):
    def name(x):return type(x) is str and re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',x) is not None
    def digest(x):return type(x) is str and re.fullmatch('[0-9a-f]{64}',x) is not None
    def real(x,lo,hi):return type(x) in (int,float) and lo<=x<=hi and math.isfinite(x)
    if type(required) is not list or not 1<=len(required)<=128 or any(not name(x) for x in required) or len(set(required))!=len(required):raise ValueError('required slices')
    if not digest(expected_distribution) or type(min_trials) is not int or not 1<=min_trials<=1000000 or not real(min_success_rate,0,1) or not real(min_worst_return,-1e6,1e6):raise ValueError('gate thresholds')
    if type(evidence) is not list or len(evidence)>128:raise ValueError('evidence list')
    rows={};keys={'slice','distribution_sha256','trials','successes','worst_return'}
    for row in evidence:
        if type(row) is not dict or set(row)!=keys:raise ValueError('evidence schema')
        key=row['slice'];n=row['trials'];k=row['successes']
        if not name(key) or key not in required or key in rows or not digest(row['distribution_sha256']):raise ValueError('evidence identity')
        if type(n) is not int or not 1<=n<=1000000 or type(k) is not int or not 0<=k<=n or not real(row['worst_return'],-1e6,1e6):raise ValueError('evidence metrics')
        rows[key]=row
    reasons=[]
    for key in sorted(required):
        if key not in rows:reasons.append(key+':missing');continue
        row=rows[key]
        for reason,failed in [('distribution',row['distribution_sha256']!=expected_distribution),('trials',row['trials']<min_trials),('success',row['successes']/row['trials']<min_success_rate),('worst-return',row['worst_return']<min_worst_return)]:
            if failed:reasons.append(key+':'+reason)
    return dict(approved=not reasons,reasons=reasons)
