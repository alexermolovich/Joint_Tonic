import re

def trace_latencies(events):
    if type(events) is not list or len(events)>200000:raise ValueError("events list")
    pairs={};clock=None
    for event in events:
        if type(event) is not tuple or len(event)!=4:raise ValueError("event tuple")
        request,boundary,stamp,event_clock=event
        if any(type(v) is not str or re.fullmatch(r"[a-z][a-z0-9_-]{0,63}",v) is None for v in (request,event_clock)):raise ValueError("identity")
        if type(boundary) is not str or boundary not in ('input','output') or type(stamp) is not int or not 0<=stamp<=2**63-1:raise ValueError("boundary/timestamp")
        if clock is not None and event_clock!=clock:raise ValueError("mixed clocks")
        clock=event_clock;pair=pairs.setdefault(request,{})
        if boundary in pair:raise ValueError("duplicate boundary")
        pair[boundary]=stamp
    out=[]
    for request,pair in sorted(pairs.items()):
        if set(pair)!={'input','output'} or pair['output']<pair['input']:raise ValueError("incomplete/negative latency")
        out.append((request,pair['output']-pair['input']))
    return out
