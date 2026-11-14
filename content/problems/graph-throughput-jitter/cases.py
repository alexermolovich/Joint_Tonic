"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def uneven(m):
 assert m.graph_throughput_jitter({'vision':[0,10,30,40]},(0,40))=={'vision':{'count':3,'throughput_hz':75000000.,'mean_interval_ns':15.,'jitter_ns':5.}}
def singleton(m):
 assert m.graph_throughput_jitter({'control':[5,15]},(0,10))=={'control':{'count':1,'throughput_hz':100000000.,'mean_interval_ns':None,'jitter_ns':None}}
def precision_empty(m):
 e=2**63-1;r=m.graph_throughput_jitter({'z':[e-10,e-9,e-7],'a':[]},(e-10,e))
 assert list(r)==['a','z'];assert r['a']['count']==0 and r['a']['jitter_ns'] is None
 assert r['z']['mean_interval_ns']==1.5 and r['z']['jitter_ns']==.5;assert m.graph_throughput_jitter({},(0,1))=={}
def scale(m):
 values=list(range(100000));before=values.copy();r=m.graph_throughput_jitter({'a':values},(0,100000))['a']
 assert r=={'count':100000,'throughput_hz':1e9,'mean_interval_ns':1.,'jitter_ns':0.};assert values==before
 r=m.graph_throughput_jitter({'a':[5,5,5]},(0,10))['a'];assert r['jitter_ns']==r['mean_interval_ns']==0
 assert type(r['count']) is int and type(r['throughput_hz']) is float
def invalid(m):
 for data,window in [([], (0,1)),({'A':[]},(0,1)),({'a':[1,0]},(0,2)),({'a':[True]},(0,2)),({'a':[1.]},(0,2)),({'a':[-1]},(0,2)),({'a':[2**63]},(0,2)),({'a':()},(0,2)),({},[0,1]),({},(1,1)),({},(False,1)),({'a':list(range(100001))},(0,100001))]:rejects(lambda:m.graph_throughput_jitter(data,window))

TESTS=[('Uneven completion intervals', 'public', uneven), ('Only one retained event', 'public', singleton), ('Nanosecond precision and empty stages', 'hidden', precision_empty), ('Scale duplicate timestamps and preservation', 'hidden', scale), ('Clock window and stage contract', 'hidden', invalid)]
