"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")

def item(version='v1',name='pose',desc=('float64',(3,),'m','base')):return {'version':version,'features':{name:desc}}
def physical(m):
 a={'robot_data':item()};b={'robot_data':item('v2',desc=('float64',(3,),'cm','tool'))};before=copy.deepcopy((a,b))
 assert m.dataset_contract_drift(a,b)==[('robot_data','','version'),('robot_data','pose','frame'),('robot_data','pose','unit')];assert (a,b)==before
def replaced(m):assert m.dataset_contract_drift({'a':item(name='x')},{'a':item(name='y'),'b':item()})==[('a','x','missing_feature'),('a','y','unexpected_feature'),('b','','unexpected_dataset')]
def all_fields(m):
 assert m.dataset_contract_drift({'a':item()},{'a':item(desc=('int64',(),'cm','tool'))})==[('a','pose',x) for x in ['dtype','frame','shape','unit']]
 assert m.dataset_contract_drift({'a':item()},{})==[('a','','missing_dataset')]
 assert m.dataset_contract_drift({},{})==[];assert m.dataset_contract_drift({'a':item()},{'a':item()})==[]
def scale(m):
 a={'d'+str(i):{'version':'v1','features':{'f'+str(j):('float64',(),'m','base') for j in range(128)}} for i in range(128)};b=copy.deepcopy(a)
 for dataset in b.values():
  for name in dataset['features']:dataset['features'][name]=('float64',(),'cm','base')
 assert m.dataset_contract_drift(a,b)==sorted((dataset,feature,'unit') for dataset,entry in a.items() for feature in entry['features'])
def invalid(m):
 bads=[[],{'A':item()},{'a':{'version':'v1','features':{}}},{'a':{'version':'v1','features':{},'extra':1}},{'a':item('')},{'a':item(desc=['float64',(3,),'m','base'])}]
 for desc in [('bad',(),'m','base'),('float64',[3],'m','base'),('float64',(True,),'m','base'),('float64',(0,),'m','base'),('float64',(10001,),'m','base'),('float64',(1,1,1,1,1),'m','base'),('float64',(),'M','base'),('float64',(),'m','')]:bads.append({'a':item(desc=desc)})
 for bad in bads:rejects(lambda:m.dataset_contract_drift({},bad));rejects(lambda:m.dataset_contract_drift(bad,{}))

TESTS=[('Physical meaning and version', 'public', physical), ('Feature replacement and dataset granularity', 'public', replaced), ('Every changed field and empty contracts', 'hidden', all_fields), ('Independent sorted grid', 'hidden', scale), ('Validate even unexpected datasets', 'hidden', invalid)]
