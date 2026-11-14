"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def overlap(m):assert m.compare_pipeline_measurements([('r',0,10)],[('r','a',1,6),('r','b',4,8)])==[('r',10,7,3,2)]
def no_spans(m):assert m.compare_pipeline_measurements([('r',100,105)],[])==[('r',5,0,5,0)]
def independent(m):
 bounds=[('z',0,12),('a',5,5)];spans=[('z','b',3,8),('z','a',1,5),('z','c',4,10),('a','zero',5,5)];before=copy.deepcopy((bounds,spans))
 assert m.compare_pipeline_measurements(bounds,spans)==[('a',0,0,0,0),('z',12,9,3,6)];assert (bounds,spans)==before
 assert m.compare_pipeline_measurements([],[])==[]
def oracle(m):
 rng=np.random.default_rng(20261114);spans=[];coverage=[0]*100
 for i in range(60):
  a=int(rng.integers(0,100));b=int(rng.integers(a,101));spans.append(('r','s'+str(i),a,b))
  for t in range(a,b):coverage[t]+=1
 covered=sum(c>0 for c in coverage);extra=sum(coverage)-covered
 assert m.compare_pipeline_measurements([('r',0,100)],spans)==[('r',100,covered,100-covered,extra)]
 e=2**63-1;assert m.compare_pipeline_measurements([('r',e-3,e)],[('r','s',e-2,e)])==[('r',3,2,1,0)]
def invalid(m):
 for b,s in [([('r',2,1)],[]),([('r',0,1),('r',0,1)],[]),([('r',0,1)],[('r','s',0,2)]),([('r',0,1)],[('x','s',0,1)]),([('r',0,1)],[('r','s',0,1),('r','s',0,1)]),([('r',True,1)],[]),([], [('r','s',0,0)]),([('A',0,1)],[]),([['r',0,1]],[])]:rejects(lambda:m.compare_pipeline_measurements(b,s))

TESTS=[('Parallel span coverage', 'public', overlap), ('No internal evidence', 'public', no_spans), ('Triple overlap and zero-length intervals', 'hidden', independent), ('Independent unit-interval union oracle', 'hidden', oracle), ('Identity interval and schema validation', 'hidden', invalid)]
