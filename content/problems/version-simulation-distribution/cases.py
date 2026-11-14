"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


import json,hashlib
CONFIG=dict(simulator='mujoco_3.3.0',asset_sha256='a'*64,seed=7,reset='episode',factors=[dict(name='yaw',unit='rad',low=-0.,high=1),dict(name='mass',unit='kg',low=1,high=2)])
def normalized(m):
 r=m.version_scenario_distribution(CONFIG);expected=copy.deepcopy(CONFIG);expected['factors']=[dict(name='mass',unit='kg',low=1.,high=2.),dict(name='yaw',unit='rad',low=0.,high=1.)];assert r['config']==expected
 payload=json.dumps(expected,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False);assert r['sha256']==hashlib.sha256(payload.encode()).hexdigest() and '-0.0' not in payload
def mass(m):
 c=copy.deepcopy(CONFIG);c['factors'][1]['low']=0;rejects(lambda:m.version_scenario_distribution(c))
def identity(m):
 c=copy.deepcopy(CONFIG);before=copy.deepcopy(c);a=m.version_scenario_distribution(c);c['factors'].reverse();c['factors'][0]['low']=1.;b=m.version_scenario_distribution(dict(reversed(list(c.items()))));assert a==b and CONFIG==before
 a['config']['factors'][0]['low']=99;assert c['factors'][0]['low']==1
 for key,value in [('seed',8),('asset_sha256','b'*64),('simulator','mujoco_3.3.1')]:
  x=copy.deepcopy(c);x[key]=value;assert m.version_scenario_distribution(x)['sha256']!=b['sha256']
def scale(m):
 c=copy.deepcopy(CONFIG);c['factors']=[dict(name='f'+str(i),unit='ratio',low=0,high=i+1) for i in range(32)];r=m.version_scenario_distribution(c);assert [f['name'] for f in r['config']['factors']]==sorted(f['name'] for f in c['factors'])
 c['factors'].append(dict(name='extra',unit='s',low=0,high=1));rejects(lambda:m.version_scenario_distribution(c))
def invalid(m):
 for key,value in [('seed',True),('seed',2**32),('reset','step'),('asset_sha256','A'*64),('simulator','bad space'),('extra',1),('factors',[])]:
  c=copy.deepcopy(CONFIG);c[key]=value;rejects(lambda:m.version_scenario_distribution(c))
 for key,value in [('unit','m'),('unit',[]),('low',np.nan),('low',10**1000),('high',-1),('high',4),('name','Mass'),('low',True)]:
  c=copy.deepcopy(CONFIG);c['factors'][0][key]=value;rejects(lambda:m.version_scenario_distribution(c))
 c=copy.deepcopy(CONFIG);c['factors']*=2;rejects(lambda:m.version_scenario_distribution(c))

TESTS=[('Canonical physical declaration', 'public', normalized), ('Positive mass required', 'public', mass), ('Order normalization storage and version identity', 'hidden', identity), ('Thirty-two independent factors', 'hidden', scale), ('Invalid schemas and physical units', 'hidden', invalid)]
