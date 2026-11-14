import re

def compare_pipeline_measurements(boundaries, spans):
    def ident(x):return type(x) is str and re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',x) is not None
    def interval(a,b):return type(a) is int and type(b) is int and 0<=a<=b<=2**63-1
    if type(boundaries) is not list or len(boundaries)>10000 or type(spans) is not list or len(spans)>100000:raise ValueError("record lists")
    limits={};groups={};seen=set()
    for row in boundaries:
        if type(row) is not tuple or len(row)!=3:raise ValueError("boundary tuple")
        key,a,b=row
        if not ident(key) or key in limits or not interval(a,b):raise ValueError("boundary identity/range")
        limits[key]=(a,b);groups[key]=[]
    for row in spans:
        if type(row) is not tuple or len(row)!=4:raise ValueError("span tuple")
        key,stage,a,b=row
        if not ident(key) or not ident(stage) or key not in limits or (key,stage) in seen or not interval(a,b):raise ValueError("span identity/range")
        if a<limits[key][0] or b>limits[key][1]:raise ValueError("span outside boundary")
        seen.add((key,stage));groups[key].append((a,b))
    out=[]
    for key,(a,b) in sorted(limits.items()):
        covered=0;right=a;summed=0
        for start,end in sorted(groups[key]):
            summed+=end-start;covered+=max(0,end-max(start,right));right=max(right,end)
        out.append((key,b-a,covered,b-a-covered,summed-covered))
    return out
