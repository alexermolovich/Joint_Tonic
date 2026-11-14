"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')
def same(a,b):
    np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)

def row(e,s,c):return dict(episode_id=e,scene_id=s,collector_id=c)
def example1(m):
 records=[row('a','s1','c1'),row('b','s2','c1'),row('c','s2','c2'),row('d','s3','c3')]
 assert m.split_scene_collector_components(records,['s1'])==dict(train_ids=['d'],test_ids=['a','b','c'],component_ids=dict(a='a',b='a',c='a',d='d'))
def example2(m):
 assert m.split_scene_collector_components([row('a','s1','c1'),row('b','s2','c2')],[])==dict(train_ids=['a','b'],test_ids=[],component_ids=dict(a='a',b='b'))
def edges(m):
 assert m.split_scene_collector_components([],[])==dict(train_ids=[],test_ids=[],component_ids={})
 r=m.split_scene_collector_components([row('b','shared','c1'),row('a','s2','shared')],['shared']);assert r['test_ids']==['b'] and r['train_ids']==['a']
 r=m.split_scene_collector_components([row('b','s','c'),row('a','s','c')],['s']);assert r['component_ids']=={'a':'a','b':'a'}
def oracle_scale(m):
 records=[row('e'+str(i),'s'+str(i//2),'c'+str((i+1)//2)) for i in range(10000)];before=copy.deepcopy(records);r=m.split_scene_collector_components(records[::-1],['s0'])
 assert not r['train_ids'] and r['test_ids']==sorted(x['episode_id'] for x in records) and set(r['component_ids'].values())=={'e0'};assert records==before
 # Independent graph flood fill on randomized smaller data.
 rng=np.random.default_rng(914);records=[row('z'+str(i),'s'+str(rng.integers(0,9)),'c'+str(rng.integers(0,9))) for i in range(25)];held=[records[0]['scene_id']];r=m.split_scene_collector_components(records,held);remaining=set(range(25));expected={};train=[];test=[]
 while remaining:
  component={remaining.pop()};changed=True
  while changed:
   additions={i for i in remaining if any(records[i]['scene_id']==records[j]['scene_id'] or records[i]['collector_id']==records[j]['collector_id'] for j in component)};changed=bool(additions);component|=additions;remaining-=additions
  names=sorted(records[i]['episode_id'] for i in component);target=test if any(records[i]['scene_id'] in held for i in component) else train;target.extend(names)
  expected.update({name:names[0] for name in names})
 assert r==dict(train_ids=sorted(train),test_ids=sorted(test),component_ids=expected)
def invalid(m):
 for records,held in [([],['s']),([row('a','s','c')],['unknown']),([row('a','s','c')]*2,[]),([row('a','s','c')],['s','s']),([row('a','s','BAD')],[])]:reject(lambda:m.split_scene_collector_components(records,held))

TESTS=[('Worked example1','public',example1),('Worked example2','public',example2),('Boundary semantics','hidden',edges),('Independent oracle,scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
