"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def boundary(m):assert m.reuse_tensor_buffers([('a',8,0,2),('b',4,2,3),('c',8,2,4)])=={'assignments':[('a',0),('b',0),('c',1)],'capacities':[8,8],'reserved_bytes':16}
def best_fit(m):assert m.reuse_tensor_buffers([('a',8,0,1),('b',4,0,1),('c',3,1,2)])=={'assignments':[('a',0),('b',1),('c',1)],'capacities':[8,4],'reserved_bytes':12}
def oracle(m):
 rng=np.random.default_rng(20261114);records=[('n'+str(i),int(rng.integers(1,100)),int(rng.integers(0,100))) for i in range(100)];records=[(n,z,s,s+int(rng.integers(1,10))) for n,z,s in records];before=copy.deepcopy(records);caps=[];ends=[];pairs=[]
 for name,size,start,end in sorted(records,key=lambda r:(r[2],r[0])):
  free=[(cap,i) for i,cap in enumerate(caps) if cap>=size and ends[i]<=start]
  if free:_,i=min(free)
  else:i=len(caps);caps.append(size);ends.append(0)
  ends[i]=end;pairs.append((name,i))
 assert m.reuse_tensor_buffers(records)==dict(assignments=pairs,capacities=caps,reserved_bytes=sum(caps));assert records==before
def scale_empty(m):
 assert m.reuse_tensor_buffers([])==dict(assignments=[],capacities=[],reserved_bytes=0)
 records=[('n'+str(i),1024,i,i+1) for i in range(10000)];r=m.reuse_tensor_buffers(records);assert r['capacities']==[1024] and r['reserved_bytes']==1024 and len(r['assignments'])==10000 and all(b==0 for _,b in r['assignments'])
def invalid(m):
 for records in [(),[('a',0,0,1)],[('a',1,1,1)],[('a',True,0,1)],[('a',1,False,1)],[('a',1,0,1),('a',2,1,2)],[('A',1,0,1)],[['a',1,0,1]]]:rejects(lambda:m.reuse_tensor_buffers(records))

TESTS=[('Half-open lifetime boundary', 'public', boundary), ('Best fit not first free', 'public', best_fit), ('Independent linear allocator oracle', 'hidden', oracle), ('Empty and large reuse chain', 'hidden', scale_empty), ('Allocation contracts', 'hidden', invalid)]
