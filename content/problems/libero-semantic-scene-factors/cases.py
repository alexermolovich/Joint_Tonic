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

def row(key,verb='pick',scene='kitchen'):return dict(task_id=key,verb=verb,object_id='cup',goal_id='tray',scene_id=scene)
def example1(m):
 r=m.semantic_scene_groups([row('a'),row('b',scene='lab'),row('c','place')]);assert r==[dict(semantic_key=('pick','cup','tray'),task_ids=['a','b'],scene_ids=['kitchen','lab'],has_scene_variation=True),dict(semantic_key=('place','cup','tray'),task_ids=['c'],scene_ids=['kitchen'],has_scene_variation=False)]
def example2(m):assert m.semantic_scene_groups([row('b'),row('a')])==[dict(semantic_key=('pick','cup','tray'),task_ids=['a','b'],scene_ids=['kitchen'],has_scene_variation=False)]
def edges(m):
 assert m.semantic_scene_groups([])==[]
 a=row('a');other=row('b');other['object_id']='tray';other['goal_id']='cup';assert len(m.semantic_scene_groups([a,other]))==2
def oracle_scale(m):
 records=[row('task'+str(j),verb='verb'+str(j%7),scene='scene'+str(j%11)) for j in range(10000)];before=copy.deepcopy(records);r=m.semantic_scene_groups(records)
 assert len(r)==7
 for result in r:
  matching=[x for x in records if x['verb']==result['semantic_key'][0]];assert result['task_ids']==sorted(x['task_id'] for x in matching);assert result['scene_ids']==sorted({x['scene_id'] for x in matching});assert result['has_scene_variation'] is True
 assert records==before
def invalid(m):
 for records in [[row('a'),row('a')],[dict(row('a'),extra=1)],[row('bad id')],[dict(row('a'),scene_id=1)]]:reject(lambda:m.semantic_scene_groups(records))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
