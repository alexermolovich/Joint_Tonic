"""Original deterministic synthetic fixtures, CC0-1.0."""
import copy
import numpy as np

def rejects(fn):
    try:fn()
    except ValueError:return
    raise AssertionError("Expected ValueError")


def seeded(m):
 r=m.sample_visual_scenarios(1,0,['a','b'],(1,2),(-1,1),(0,2));assert r['texture']==['b'];np.testing.assert_allclose(r['brightness'],[1.2697867137638703]);np.testing.assert_allclose(r['yaw'],[-.9180529521276106]);np.testing.assert_array_equal(r['distractors'],[0])
def fixed(m):
 r=m.sample_visual_scenarios(2,7,['only'],(2,2),(0,0),(3,3));assert r['texture']==['only']*2;np.testing.assert_array_equal(r['brightness'],[2,2]);np.testing.assert_array_equal(r['yaw'],[0,0]);np.testing.assert_array_equal(r['distractors'],[3,3])
def scale_rng(m):
 np.random.seed(3);expected=np.random.random(3);np.random.seed(3);textures=['a','b','c'];r=m.sample_visual_scenarios(10000,99,textures,(0,10),(-np.pi,np.pi),(0,100));np.testing.assert_array_equal(np.random.random(3),expected);assert textures==['a','b','c']
 u=np.random.Generator(np.random.PCG64(99)).random((10000,4));assert r['texture']==[textures[int(x*3)] for x in u[:,0]];np.testing.assert_allclose(r['brightness'],10*u[:,1]);np.testing.assert_allclose(r['yaw'],-np.pi+2*np.pi*u[:,2]);np.testing.assert_array_equal(r['distractors'],np.floor(u[:,3]*101).astype(np.int64))
def empty_storage(m):
 r=m.sample_visual_scenarios(0,0,['a'],(0,1),(0,1),(0,1));assert r['texture']==[];assert r['brightness'].shape==(0,) and r['brightness'].dtype==np.float64 and r['distractors'].dtype==np.int64
 r=m.sample_visual_scenarios(5,0,['a'],(0,1),(0,1),(0,1));assert not np.shares_memory(r['brightness'],r['yaw'])
def invalid(m):
 good=[0,0,['a'],(0,1),(0,1),(0,1)]
 for i,value in [(0,True),(0,10001),(1,-1),(2,['a','a']),(2,['A']),(3,(2,1)),(3,(0,np.inf)),(3,(0,10**1000)),(4,(-4,0)),(5,(0,101)),(5,(False,1))]:
  a=copy.deepcopy(good);a[i]=value;rejects(lambda:m.sample_visual_scenarios(*a))

TESTS=[('Known seed four factors', 'public', seeded), ('Fixed physical intervals', 'public', fixed), ('Scale independent draw oracle and RNG preservation', 'hidden', scale_rng), ('Empty shapes and storage', 'hidden', empty_storage), ('Invalid physical bounds and IDs', 'hidden', invalid)]
