import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def good(m):
    r=m.capture_health(np.full((1,1,1,3),128,np.uint8),[0],[0],[1000],1000,.1);assert not r['flags'].any();assert r['ready'];assert_array_equal(r['saturation_fraction'],[0])
def gaps(m):
    x=np.full((2,1,1,3),128,np.uint8);x[1]=255;r=m.capture_health(x,[0,.2],[0,2],[1000,1000],1000,.1);assert_array_equal(r['flags'],[[False]*4,[True,True,False,True]]);assert not r['ready']
def boundary(m):
    x=np.full((2,1,20,3),128,np.uint8);x[0].reshape(-1)[:57]=255;x[1].reshape(-1)[:58]=255;r=m.capture_health(x,[0,.125],[4,5],[950,1050],1000,.125);assert_allclose(r['saturation_fraction'],[.95,58/60]);assert_array_equal(r['flags'][:,3],[False,True]);assert not r['flags'][:,:3].any()
    x=np.full((3,1,1,3),128,np.uint8);r=m.capture_health(x,[1,1,.5],[0,1,1],[1000]*3,1000,.1);assert_array_equal(r['flags'][1:,:2],[[True,False],[True,True]])
def scale(m):
    x=np.full((64,64,128,3),128,np.uint8)[:,:,::2,:];saved=x.copy();r=m.capture_health(x,np.arange(64)*.01,np.arange(64),np.full(64,1000.),1000,.1);assert r['ready'];assert_array_equal(x,saved);assert not np.shares_memory(r['flags'],x)
    r=m.capture_health(np.empty((0,1,1,3),np.uint8),[],np.empty(0,int),[],1000,.1);assert not r['ready'] and r['flags'].shape==(0,4)
def invalid(m):
    x=np.full((1,1,1,3),128,np.uint8)
    for a in [(x.astype(float),[0],[0],[1000],1000,.1),(x,[np.nan],[0],[1000],1000,.1),(x,[0],[0],[1000],10**1000,.1)]:bad(lambda:m.capture_health(*a))
TESTS=[('Usable optical capture','public',good),('Separate timing ID and saturation failures','public',gaps),('Exact saturation exposure and timing boundaries','hidden',boundary),('Scale and empty captures','hidden',scale),('Invalid capture representation','hidden',invalid)]
