import math
import re

def select_pareto_model(records, min_accuracy, max_latency_ms):
    def real(x,lo,hi,strict=False):return type(x) in (int,float) and (lo<x<=hi if strict else lo<=x<=hi) and math.isfinite(x)
    if type(records) is not list or len(records)>1000 or not real(min_accuracy,0,1) or not real(max_latency_ms,0,1000000,True):raise ValueError('records or limits')
    names=set()
    for row in records:
        if type(row) is not tuple or len(row)!=3:raise ValueError('model record')
        key,a,l=row
        if type(key) is not str or re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',key) is None or key in names or not real(a,0,1) or not real(l,0,1000000,True):raise ValueError('model metric')
        names.add(key)
    frontier=sorted(key for key,a,l in records if not any(aa>=a and ll<=l and (aa>a or ll<l) for _,aa,ll in records))
    feasible=[(-a,l,key) for key,a,l in records if a>=min_accuracy and l<=max_latency_ms]
    return dict(frontier=frontier,selected=min(feasible)[2] if feasible else None)
