"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):np.testing.assert_array_equal(a,b)

def dataset(k='a'):return dict(dataset_id=k,intended_uses=['research'],prohibited_uses=['commercial'],embodiments=['fr3'],contains_personal_data=False,consent='unknown',license_known=True)
def example1(m):assert m.data_use_review_flags([dataset()],'research','fr3')==[dict(dataset_id='a',flags=[],needs_review=False)]
def example2(m):
 d=dataset();d['contains_personal_data']=True;d['license_known']=False
 assert m.data_use_review_flags([d],'commercial','panda')==[dict(dataset_id='a',flags=['consent_unknown','outside_intended_use','prohibited_use','unknown_license','unsupported_embodiment'],needs_review=True)]
def edges(m):
 d=dataset();d['prohibited_uses']=['research'];assert m.data_use_review_flags([d],'research','fr3')[0]['flags']==['prohibited_use']
 d=dataset();d['consent']='denied';assert not m.data_use_review_flags([d],'research','fr3')[0]['flags'];d['contains_personal_data']=True;assert m.data_use_review_flags([d],'research','fr3')[0]['flags']==['consent_denied']
 assert m.data_use_review_flags([],'research','fr3')==[]
def oracle_scale(m):
 records=[];expected=[]
 for i in range(1000):
  d=dataset('d'+str(i));d['contains_personal_data']=bool(i%2);d['license_known']=bool(i%3);d['consent']='granted' if i%5==0 else 'unknown';records.append(d)
  flags=[]
  if i%3==0:flags.append('unknown_license')
  if i%2 and i%5:flags.append('consent_unknown')
  expected.append(dict(dataset_id=d['dataset_id'],flags=sorted(flags),needs_review=bool(flags)))
 before=copy.deepcopy(records);assert m.data_use_review_flags(records[::-1],'research','fr3')==sorted(expected,key=lambda d:d['dataset_id']);assert records==before

def invalid(m):
 for key,value in [('contains_personal_data',1),('license_known','yes'),('consent',[]),('consent','maybe'),('intended_uses',['research','research']),('embodiments',[None])]:
  d=dataset();d[key]=value;reject(lambda:m.data_use_review_flags([d],'research','fr3'))
 reject(lambda:m.data_use_review_flags([dataset(),dataset()],'research','fr3'));reject(lambda:m.data_use_review_flags([],'BAD','fr3'))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
