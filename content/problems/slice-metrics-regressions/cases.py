"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def hidden(m):
 r=m.compare_slice_regressions(np.array([0,0,1],dtype=np.int64),np.array([2.,2.,2.]),np.array([0.,0.,5.]),2,0);np.testing.assert_array_equal(r['counts'],[2,1]);np.testing.assert_array_equal(r['mean_delta'],[-2,3]);np.testing.assert_array_equal(r['regressed'],[False,True]);assert abs(r['overall_delta']+1/3)<1e-12 and r['complete']
def missing(m):
 r=m.compare_slice_regressions(np.array([0],dtype=np.int64),np.array([1.]),np.array([1.5]),2,.5);np.testing.assert_allclose(r['mean_delta'],[.5,np.nan],equal_nan=True);assert not r['regressed'].any() and not r['complete'] and r['overall_delta']==.5
def empty(m):
 r=m.compare_slice_regressions(np.array([],dtype=np.int64),np.array([],dtype=float),np.array([],dtype=float),3,0);assert r['overall_delta'] is None and not r['complete'] and np.isnan(r['mean_delta']).all() and not r['regressed'].any()
def scale(m):
 ids=(np.arange(200000,dtype=np.int64)%12)[::2];b=np.full(100000,10.);c=b+(ids-5);before=c.copy();r=m.compare_slice_regressions(ids,b,c,12,0)
 for j in range(12):
  n=int((ids==j).sum());assert r['counts'][j]==n
  if n:assert r['mean_delta'][j]==j-5 and r['regressed'][j]==(j>5)
  else:assert np.isnan(r['mean_delta'][j])
 assert abs(r['overall_delta']-sum(float(x-5) for x in ids)/100000)<1e-12;np.testing.assert_array_equal(c,before);assert not np.shares_memory(r['mean_delta'],c)
def invalid(m):
 good=[np.array([0],dtype=np.int64),np.ones(1),np.ones(1),1,0]
 for i,value in [(0,np.array([1],dtype=np.int64)),(0,np.array([0],dtype=np.int32)),(1,np.array([-1.])),(2,np.array([np.nan])),(2,np.ones(2)),(3,True),(4,-1),(4,10**1000)]:
  a=[v.copy() if isinstance(v,np.ndarray) else v for v in good];a[i]=value;rejects(lambda:m.compare_slice_regressions(*a))

TESTS=[('Pooled improvement with rare slice regression', 'public', hidden), ('Missing slice and inclusive tolerance', 'public', missing), ('No paired evidence', 'hidden', empty), ('Independent constant-delta slice oracle at scale', 'hidden', scale), ('Invalid paired evaluation schema', 'hidden', invalid)]
