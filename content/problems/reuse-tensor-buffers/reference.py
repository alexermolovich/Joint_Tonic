import re
import heapq
import bisect

def reuse_tensor_buffers(tensors):
    if type(tensors) is not list or len(tensors)>10000:raise ValueError("tensor list")
    names=set()
    for record in tensors:
        if type(record) is not tuple or len(record)!=4:raise ValueError("tensor tuple")
        name,size,start,end=record
        if type(name) is not str or re.fullmatch(r'[a-z][a-z0-9_-]{0,63}',name) is None or name in names:raise ValueError("identity")
        if type(size) is not int or not 1<=size<=10**9 or type(start) is not int or type(end) is not int or not 0<=start<end<=10**9:raise ValueError("size/lifetime")
        names.add(name)
    busy=[];free=[];capacities=[];assignments=[]
    for name,size,start,end in sorted(tensors,key=lambda row:(row[2],row[0])):
        while busy and busy[0][0]<=start:
            _,buffer=heapq.heappop(busy);bisect.insort(free,(capacities[buffer],buffer))
        index=bisect.bisect_left(free,(size,-1))
        if index<len(free):_,buffer=free.pop(index)
        else:buffer=len(capacities);capacities.append(size)
        heapq.heappush(busy,(end,buffer));assignments.append((name,buffer))
    return dict(assignments=assignments,capacities=capacities,reserved_bytes=sum(capacities))
