"""Original deterministic synthetic fixtures; CC0-1.0."""
import copy
import math
import numpy as np

def reject(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected ValueError')

def same(a,b):np.testing.assert_allclose(a,b,rtol=1e-10,atol=1e-10,equal_nan=True)
def f(x):return np.array(x,dtype=np.float64)
def i(x):return np.array(x,dtype=np.int64)
def b(x):return np.array(x,dtype=bool)

def unchanged(before,after):
    for x,y in zip(before,after):np.testing.assert_array_equal(x,y)

def clip(key,start,end,video='v'):return dict(clip_id=key,video_id=video,start_ns=start,end_ns=end)
def example1(m):assert m.temporal_split_groups([clip('a',0,10),clip('b',10,20),clip('c',21,30)],['b'],0)==[dict(clip_id='a',group_id='a',split='test'),dict(clip_id='b',group_id='a',split='test'),dict(clip_id='c',group_id='c',split='train')]
def example2(m):assert m.temporal_split_groups([clip('a',0,10),clip('b',15,20),clip('c',25,30)],['c'],5)==[dict(clip_id=x,group_id='a',split='test') for x in 'abc']
def edges(m):
 hi=2**63-1;rows=[clip('z',0,10),clip('a',0,100),clip('b',90,110),clip('c',0,10,'other')];r=m.temporal_split_groups(rows,['z'],0);assert [x['group_id'] for x in r]==['a','a','c','a'];assert r[2]['split']=='train'
 assert m.temporal_split_groups([],[],0)==[]
 r=m.temporal_split_groups([clip('a',0,1),clip('b',hi-1,hi)],['b'],hi);assert all(x['split']=='test' for x in r)
def oracle_scale(m):
 rows=[clip('c'+str(j),j*2,j*2+1) for j in range(100000)];before=copy.deepcopy(rows);r=m.temporal_split_groups(rows,['c99999'],1);assert len(r)==100000 and all(x['group_id']=='c0' and x['split']=='test' for x in r);assert rows==before
 rng=np.random.default_rng(938);rows=[clip('c'+str(j),int(j*3),int(j*3+rng.integers(1,12)),video='v'+str(j%2)) for j in range(40)];neighbors={x['clip_id']:{x['clip_id']} for x in rows}
 for a in rows:
  for z in rows:
   if a['video_id']==z['video_id'] and max(0,max(a['start_ns'],z['start_ns'])-min(a['end_ns'],z['end_ns']))<=2:neighbors[a['clip_id']].add(z['clip_id'])
 for _ in rows:
  for key in neighbors:neighbors[key]=set.union(*(neighbors[k] for k in neighbors[key]))
 r=m.temporal_split_groups(rows,['c20'],2)
 for out in r:assert out['group_id']==min(neighbors[out['clip_id']]);assert out['split']==('test' if 'c20' in neighbors[out['clip_id']] else 'train')
def invalid(m):
 for rows,held,g in [([clip('a',0,1),clip('a',1,2)],[],0),([clip('a',0,1)],['z'],0),([clip('a',0,1)],['a','a'],0),([clip('a',1,1)],[],0),([clip('a',0,1)],[],-1),([clip('a',0,1)],[],True)]:reject(lambda:m.temporal_split_groups(rows,held,g))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
