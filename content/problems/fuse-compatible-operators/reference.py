import math
import re

def fuse_operator_chains(nodes):
    if type(nodes) is not list or len(nodes)>10000:raise ValueError("nodes list")
    by_id={};consumers={}
    for row in nodes:
        if type(row) is not tuple or len(row)!=4:raise ValueError("node tuple")
        key,op,parent,shape=row
        if type(key) is not str or re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',key) is None or key in by_id:raise ValueError("node identity")
        if type(op) is not str or op not in ('input','scale','relu','sigmoid','barrier'):raise ValueError("operator")
        if type(shape) is not tuple or not 1<=len(shape)<=4 or any(type(d) is not int or not 1<=d<=4096 for d in shape) or math.prod(shape)>1000000:raise ValueError("shape")
        if op=='input':
            if parent is not None:raise ValueError("input parent")
        else:
            if type(parent) is not str or parent not in by_id:raise ValueError("topological parent")
            if op!='barrier' and shape!=by_id[parent][2]:raise ValueError("unsupported shape change")
            consumers[parent]+=1
        by_id[key]=(op,parent,shape);consumers[key]=0
    groups=[];group_of={};fusible=('scale','relu','sigmoid')
    for key,op,parent,shape in nodes:
        if op in fusible and by_id[parent][0] in fusible and consumers[parent]==1:
            index=group_of[parent];groups[index].append(key)
        else:index=len(groups);groups.append([key])
        group_of[key]=index
    return [tuple(group) for group in groups]
