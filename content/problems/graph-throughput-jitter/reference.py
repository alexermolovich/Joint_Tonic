import math
import re

def graph_throughput_jitter(completions, window):
    def stamp(x):return type(x) is int and 0<=x<=2**63-1
    if type(completions) is not dict or len(completions)>128 or type(window) is not tuple or len(window)!=2 or not all(stamp(t) for t in window) or window[0]>=window[1]:raise ValueError("window/stages")
    total=0
    for key,values in completions.items():
        if type(key) is not str or re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',key) is None or type(values) is not list or any(not stamp(t) for t in values):raise ValueError("stage/timestamps")
        if any(b<a for a,b in zip(values,values[1:])):raise ValueError("timestamp order")
        total+=len(values)
    if total>100000:raise ValueError("event budget")
    start,end=window;out={}
    for key,values in sorted(completions.items()):
        retained=[t for t in values if start<=t<end];gaps=[b-a for a,b in zip(retained,retained[1:])]
        mean=math.fsum(gaps)/len(gaps) if gaps else None
        jitter=math.sqrt(math.fsum((d-mean)**2 for d in gaps)/len(gaps)) if gaps else None
        out[key]=dict(count=len(retained),throughput_hz=len(retained)*1e9/(end-start),mean_interval_ns=mean,jitter_ns=jitter)
    return out
