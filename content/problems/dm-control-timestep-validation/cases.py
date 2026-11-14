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

def good():return dict(step_type=2,reward=1,discount=1,observation=f([0]))
def example1(m):assert m.validate_control_timestep(good(),1)==[]
def example2(m):assert m.validate_control_timestep(dict(step_type=0,reward=0,observation=f([0]),extra=True),1)==['invalid:reward','missing:discount','unexpected:extra']
def edges(m):
 assert m.validate_control_timestep(dict(step_type=0,reward=None,discount=None,observation=np.ones(2,dtype=np.float32)),2)==[]
 assert m.validate_control_timestep({},1)==['missing:discount','missing:observation','missing:reward','missing:step_type']
 r=good();r.update(step_type=True,reward='bad',discount='bad');assert m.validate_control_timestep(r,1)==['invalid:step_type']
 r=good();r['observation']=f([np.nan]);r['reward']=True;r['discount']=-.1;assert m.validate_control_timestep(r,1)==['invalid:discount','invalid:observation','invalid:reward']
 for step in [1,2]:
  for discount in [0,.5,1]:
   r=good();r.update(step_type=step,discount=discount);assert m.validate_control_timestep(r,1)==[]
def oracle_scale(m):
 obs=np.arange(8192,dtype=np.float64)[::2];r=good();r['observation']=obs;before=copy.deepcopy(r)
 for key in ['a','b','c','d','e','f','g','h','i','j','k','l']:r[key]=0
 assert m.validate_control_timestep(r,4096)==['unexpected:'+k for k in 'abcdefghijkl'];unchanged([before['observation']],[obs]);assert r['step_type']==2
 for key in ['reward','discount']:
  for value in [None,np.float64(1),float('inf'),10**1000]:
   a=good();a[key]=value;assert m.validate_control_timestep(a,1)==['invalid:'+key]
def invalid(m):
 for r,d in [([],1),({1:0},1),({str(k):0 for k in range(17)},1),(good(),0),(good(),4097),(good(),True),(good(),np.int64(1))]:reject(lambda:m.validate_control_timestep(r,d))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
