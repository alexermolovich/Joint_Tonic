"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def base():
 return {'scenario':'server','model_sha256':'a'*64,'expected_queries':10,'completed_queries':10,'failed_queries':0,'duration_ns':100,'quality':.8},{'scenario':'server','model_sha256':'a'*64,'min_queries':10,'min_duration_ns':100,'min_quality':.8}
def equality(m):
 r,p=base();before=copy.deepcopy((r,p));assert m.benchmark_run_rejections(r,p)==[];assert (r,p)==before
def multiple(m):
 r,p=base();r.update(completed_queries=8,failed_queries=1,duration_ns=99,quality=.79);p['min_queries']=9
 assert m.benchmark_run_rejections(r,p)==['failed_queries','incomplete','insufficient_duration','insufficient_queries','quality']
def independent(m):
 r,p=base();r.update(scenario='single_stream',model_sha256='b'*64)
 assert m.benchmark_run_rejections(r,p)==['model','scenario']
 r,p=base();r.update(completed_queries=0,expected_queries=0,duration_ns=0,quality=0)
 assert m.benchmark_run_rejections(r,p)==['insufficient_duration','insufficient_queries','quality']
def invalid(m):
 for which,key,value in [(0,'expected_queries',True),(0,'completed_queries',11),(0,'failed_queries',-1),(0,'duration_ns',2**63),(0,'duration_ns',1.),(1,'min_queries',0),(1,'min_duration_ns',0),(0,'quality',np.nan),(1,'min_quality',np.inf),(0,'quality',True),(0,'quality',10**1000),(0,'model_sha256','A'*64),(1,'scenario','offline')]:
  r,p=base();[r,p][which][key]=value;rejects(lambda:m.benchmark_run_rejections(r,p))
 r,p=base();r['extra']=1;rejects(lambda:m.benchmark_run_rejections(r,p));rejects(lambda:m.benchmark_run_rejections([],p))
def exhaustive(m):
 for e in range(6):
  for c in range(e+1):
   for f in range(e-c+1):
    r,p=base();r.update(expected_queries=e,completed_queries=c,failed_queries=f);p['min_queries']=3
    expected=[]
    if f:expected.append('failed_queries')
    if c+f!=e:expected.append('incomplete')
    if c<3:expected.append('insufficient_queries')
    assert m.benchmark_run_rejections(r,p)==expected

TESTS=[('Equality passes', 'public', equality), ('Failures and unfinished work', 'public', multiple), ('Identity and empty evidence gates', 'hidden', independent), ('Malformed evidence rejects before gating', 'hidden', invalid), ('Exhaustive small counter accounting', 'hidden', exhaustive)]
