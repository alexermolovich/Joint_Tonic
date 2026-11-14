"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def one(m):
 r=m.scenario_coverage(np.array([0],dtype=np.int64),np.array([True]),2);np.testing.assert_array_equal(r['counts'],[1,0]);np.testing.assert_allclose(r['success_rate'],[1,np.nan],equal_nan=True);np.testing.assert_allclose(r['wilson'],[[.20654329147389294,1],[np.nan,np.nan]],equal_nan=True);assert r['coverage']==.5
def half(m):
 r=m.scenario_coverage(np.array([0,0],dtype=np.int64),np.array([True,False]),1);np.testing.assert_allclose(r['wilson'],[[.09452865480086614,.9054713451991339]]);assert r['coverage']==1
def boundaries(m):
 r=m.scenario_coverage(np.array([],dtype=np.int64),np.array([],dtype=bool),3);assert r['coverage']==0 and np.isnan(r['wilson']).all()
 r=m.scenario_coverage(np.array([0,1],dtype=np.int64),np.array([False,True]),2);np.testing.assert_allclose(r['wilson'][0],1-r['wilson'][1,::-1],atol=1e-15)
def scale(m):
 ids=(np.arange(200000,dtype=np.int64)%16)[::2];y=(np.arange(200000)%3==0)[::2];ic=ids.copy();yc=y.copy();r=m.scenario_coverage(ids,y,32)
 for b in range(32):
  vals=y[ids==b];n=len(vals);assert r['counts'][b]==n
  if n:
   k=int(vals.sum());p=k/n;z=1.96;center=(k+z*z/2)/(n+z*z);half=z*((k*(n-k)/n+z*z/4)**.5)/(n+z*z);np.testing.assert_allclose(r['wilson'][b],[max(0,center-half),min(1,center+half)])
 np.testing.assert_array_equal(ids,ic);np.testing.assert_array_equal(y,yc);assert r['coverage']==.25 and r['counts'].dtype==np.int64
def invalid(m):
 for ids,y,b in [(np.array([0],dtype=np.int32),np.array([True]),1),(np.array([0],dtype=np.int64),np.array([1]),1),(np.array([-1],dtype=np.int64),np.array([True]),1),(np.array([1],dtype=np.int64),np.array([True]),1),(np.array([0],dtype=np.int64),np.array([],dtype=bool),1),(np.array([0],dtype=np.int64),np.array([True]),True)]:rejects(lambda:m.scenario_coverage(ids,y,b))

TESTS=[('One success and missing bucket', 'public', one), ('One success in two trials', 'public', half), ('Empty evidence and complement symmetry', 'hidden', boundaries), ('Independent count formula at scale', 'hidden', scale), ('Invalid coverage contract', 'hidden', invalid)]
