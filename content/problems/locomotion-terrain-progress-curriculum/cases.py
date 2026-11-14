import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def one(m):
    r=m.update_terrain_levels([0,2],[[6,0],[6,0]],[[0,0],[0,0]],[[1,0],[1,0]],[True,True],10,10,3,[0,.4]);assert_array_equal(r['levels'],[1,1]);assert_array_equal(r['move_up'],[True,True]);assert_array_equal(r['move_down'],[False,False]);assert_array_equal(r['reassigned'],[False,True]);assert_array_equal(r['distance'],[6,6])
def low(m):
    r=m.update_terrain_levels([0],[[0,0]],[[0,0]],[[1,0]],[True],10,10,3,[0]);assert_array_equal(r['move_down'],[True]);assert_array_equal(r['levels'],[0])
def oracle(m):
    rng=np.random.default_rng(560);n=16384;level=rng.integers(0,8,n);p=rng.normal(size=(n,4))[:,::2]*5;o=rng.normal(size=(n,2));c=rng.normal(size=(n,2));mask=rng.random(n)>.2;draw=rng.random(n);before=level.copy();out=m.update_terrain_levels(level,p,o,c,mask,10,10,8,draw)
    for i in range(n):
        distance=sum(float(x)**2 for x in p[i]-o[i])**.5;up=bool(mask[i] and distance>5);down=bool(mask[i] and distance<sum(float(x)**2 for x in c[i])**.5*5 and not up);candidate=int(level[i])+int(up)-int(down);reassigned=bool(mask[i] and candidate>=8);expected=int(draw[i]*8) if reassigned else max(candidate,0);assert out['levels'][i]==expected and out['move_up'][i]==up and out['move_down'][i]==down and out['reassigned'][i]==reassigned
    assert_array_equal(level,before);assert not np.shares_memory(out['levels'],level)
    r=m.update_terrain_levels([2,2,2,1,1],[[6,0],[6,0],[6,0],[5,0],[0,0]],np.zeros((5,2)),[[100,0],[1,0],[1,0],[1,0],[0,0]],[True,True,False,True,True],10,10,3,[np.nextafter(1.,0.),0,0,0,0]);assert_array_equal(r['levels'],[2,0,2,1,1]);assert_array_equal(r['move_down'],[False]*5);assert_array_equal(r['reassigned'],[True,True,False,False,False])
    r=m.update_terrain_levels(np.empty(0,int),np.empty((0,2)),np.empty((0,2)),np.empty((0,2)),np.empty(0,bool),1,1,1,np.empty(0));assert r['levels'].shape==(0,)
def invalid(m):
    for level,draw,length,count in [([3],[0],1,3),([0],[1],1,3),([0],[0],0,3),([0],[0],1,True),([0],[0],10**1000,3)]:bad(lambda:m.update_terrain_levels(level,[[0,0]],[[0,0]],[[0,0]],[False],length,1,count,draw))
TESTS=[('Promotion and top-level reassignment','public',one),('Minimum-level demotion','public',low),('Scalar curriculum oracle scale precedence exact thresholds and recorded bounds','hidden',oracle),('Invalid curriculum state and parameters','hidden',invalid)]
