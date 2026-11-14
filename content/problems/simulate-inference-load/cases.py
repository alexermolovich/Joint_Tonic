"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def single(m):assert m.simulate_inference_load([3,2,4],'single_stream')==[(0,0,3,3),(3,3,5,2),(5,5,9,4)]
def server(m):assert m.simulate_inference_load([3,2,4],'server',[0,1,8])==[(0,0,3,3),(1,3,5,4),(8,8,12,4)]
def boundaries(m):
 end=2**63-1;assert m.simulate_inference_load([3,4],'server',[end,end])==[(end,end,end+3,3),(end,end+3,end+7,7)]
 assert m.simulate_inference_load([],'single_stream')==[];assert m.simulate_inference_load([],'server',[])==[]
def oracle(m):
 durations=[1+(i%7) for i in range(100000)];arrivals=[i//3 for i in range(100000)];before=(durations.copy(),arrivals.copy());out=m.simulate_inference_load(durations,'server',arrivals)
 assert len(out)==len(durations);wait=0;previous_arrival=0
 for i,(arrival,start,finish,latency) in enumerate(out):
  if i:wait=max(0,wait+durations[i-1]-(arrivals[i]-previous_arrival))
  assert (arrival,start,finish,latency)==(arrivals[i],arrivals[i]+wait,arrivals[i]+wait+durations[i],wait+durations[i]);assert all(type(x) is int for x in out[i]);previous_arrival=arrivals[i]
 assert (durations,arrivals)==before
def invalid(m):
 for ds,mode,arrivals in [((1,),'server',[0]),([True],'server',[0]),([0],'server',[0]),([10**12+1],'server',[0]),([1],'bad',None),([1],'single_stream',[]),([1],'server',None),([1],'server',[0,1]),([1],'server',[True]),([1],'server',[-1]),([1],'server',[2**63]),([1,1],'server',[2,1])]:rejects(lambda:m.simulate_inference_load(ds,mode,arrivals))

TESTS=[('Closed-loop schedule', 'public', single), ('Queue and idle schedule', 'public', server), ('Ties empty and arbitrary-size output timestamps', 'hidden', boundaries), ('Independent waiting recurrence at scale', 'hidden', oracle), ('Arrival/service contract', 'hidden', invalid)]
