"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def correlation(m):
 events=[('b','output',150,'mono'),('a','input',100,'mono'),('b','input',110,'mono'),('a','output',160,'mono')];before=copy.deepcopy(events)
 assert m.trace_latencies(events)==[('a',60),('b',40)];assert events==before
def precision(m):assert m.trace_latencies([('tiny','input',2**63-3,'mono'),('tiny','output',2**63-1,'mono'),('same','input',8,'mono'),('same','output',8,'mono')])==[('same',0),('tiny',2)]
def empty(m):assert m.trace_latencies([])==[]
def arbitrary_order(m):
 events=[]
 for i in range(10000):events.extend([('r'+str(i),'input',i*100,'mono'),('r'+str(i),'output',i*100+i%90,'mono')])
 np.random.default_rng(20261113).shuffle(events)
 assert m.trace_latencies(events)==sorted(('r'+str(i),i%90) for i in range(10000))
def invalid(m):
 for e in [(),[('a','input',0,'mono')],[('a','input',0,'mono'),('a','input',0,'mono'),('a','output',1,'mono')],[('a','input',2,'mono'),('a','output',1,'mono')],[('a','input',0,'mono'),('a','output',1,'other')],[('a','other',0,'mono')],[('A','input',0,'mono')],[['a','input',0,'mono']],[('a','input',True,'mono')],[('a','input',2**63,'mono')],[('a','input',-1,'mono')],[('a','input',1.,'mono')]]:rejects(lambda:m.trace_latencies(e))

TESTS=[('Correlation rather than list order', 'public', correlation), ('Integer precision and zero duration', 'public', precision), ('Empty trace', 'hidden', empty), ('Independent correlated trace at scale', 'hidden', arbitrary_order), ('Missing duplicate mixed-clock malformed traces', 'hidden', invalid)]
