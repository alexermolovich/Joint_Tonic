import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.source_embodiment_metrics([0,0,2],[0,0,1],[True,False,True],[2,4,3],2);assert_array_equal(r['count'],[[2,0],[0,0],[0,1]]);assert r['success_rate'][0,0]==.5 and r['p95_latency_ms'][0,0]==4;assert_allclose(r['overall_success'],2/3);assert r['worst_observed_success']==.5

def empty(m):
    r=m.source_embodiment_metrics(np.array([],int),np.array([],int),np.array([],bool),[],1);assert r['overall_success'] is None and np.isnan(r['success_rate']).all()
def scale(m):
    s=np.arange(20000)[::2]%3;e=np.arange(10000)%16;y=np.ones(10000,bool);t=np.arange(10000)%100;r=m.source_embodiment_metrics(s,e,y,t,16);assert r['count'].sum()==10000 and r['overall_success']==1 and r['worst_observed_success']==1;assert np.all(r['success_rate']==1)
def invalid(m):
    for a in [([3],[0],[True],[0],1),([0],[-1],[True],[0],1),([0],[0],[True],[-1],1),([0],[0],[1],[0],1)]:bad(lambda:m.source_embodiment_metrics(*a))
TESTS=[('Source and embodiment slices','public',one),('No evidence','public',empty),('Scale and micro aggregation','hidden',scale),('Invalid evaluations','hidden',invalid)]

def p95_rank(m):
    r=m.source_embodiment_metrics(np.zeros(20,int),np.zeros(20,int),np.ones(20,bool),np.arange(20,0,-1),1);assert r["p95_latency_ms"][0,0]==19
TESTS.append(("Within-slice nearest-rank percentile", "hidden", p95_rank))
