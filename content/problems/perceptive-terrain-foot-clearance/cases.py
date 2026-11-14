import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    try: fn()
    except ValueError: return
    raise AssertionError("expected ValueError")

def first(m):
    r=m.terrain_clearance_report([[[[0,0,.2]],[[0,0,.05]]]],np.zeros((1,2,1)),np.ones((1,2,1),bool),np.ones((1,2,1),bool),[0],[.1,.1],2);assert_allclose(r['clearance'],[[[.2],[.05]]]);assert_array_equal(r['counts'],[2,0]);assert_allclose(r['mean_clearance'],[.125,np.nan]);assert_allclose(r['min_clearance'],[.05,np.nan]);assert_allclose(r['violation_rate'],[.5,np.nan])

def stance(m):
    r=m.terrain_clearance_report([[[[0,0,.1]],[[0,0,-.2]]]],np.zeros((1,2,1)),np.array([[[1],[0]]],bool),np.ones((1,2,1),bool),[0],[.1],1);assert_allclose(r['clearance'],[[[.1],[np.nan]]]);assert_array_equal(r['counts'],[1]);assert_allclose(r['mean_clearance'],[.1]);assert_allclose(r['min_clearance'],[.1]);assert_allclose(r['violation_rate'],[0])

def oracle(m):
    rng=np.random.default_rng(563);p=rng.normal(size=(128,256,4,6))[:,:,:,::2];h=rng.normal(size=(128,256,8))[:,:,::2];s=rng.random(h.shape)>.3;o=rng.random(h.shape)>.2;ids=rng.integers(0,7,128);tau=rng.random(8);before=p.copy();r=m.terrain_clearance_report(p,h,s,o,ids,tau,8);groups=[[] for _ in range(8)]
    for b,t,f in np.ndindex(h.shape):
        if s[b,t,f] and o[b,t,f]:groups[ids[b]].append(p[b,t,f,2]-h[b,t,f]);assert_allclose(r['clearance'][b,t,f],p[b,t,f,2]-h[b,t,f])
        else:assert np.isnan(r['clearance'][b,t,f])
    for k,values in enumerate(groups):
        assert r['counts'][k]==len(values)
        if values:assert_allclose(r['mean_clearance'][k],sum(values)/len(values));assert_allclose(r['min_clearance'][k],min(values));assert_allclose(r['violation_rate'][k],sum(v<tau[k] for v in values)/len(values))
        else:assert np.isnan([r['mean_clearance'][k],r['min_clearance'][k],r['violation_rate'][k]]).all()
    assert_array_equal(p,before)
    for value in r.values():
        for a in [p,h,s,o,ids,tau]:assert not np.shares_memory(value,a)

def boundaries(m):
    r=m.terrain_clearance_report(np.empty((0,1,1,3)),np.empty((0,1,1)),np.empty((0,1,1),bool),np.empty((0,1,1),bool),np.empty(0,int),[0],1);assert r['clearance'].shape==(0,1,1) and r['counts'][0]==0 and np.isnan(r['violation_rate'][0])
    p=np.array([[[[0.,0.,-.2],[0,0,.1]]]]);h=np.zeros((1,1,2));r=m.terrain_clearance_report(p,h,np.ones(h.shape,bool),np.ones(h.shape,bool),[0],[.1],1);assert_allclose(r['min_clearance'],[-.2]);assert_allclose(r['violation_rate'],[.5]);r=m.terrain_clearance_report(p,h,np.zeros(h.shape,bool),np.ones(h.shape,bool),[0],[.1],1);assert r['counts'][0]==0 and np.isnan(r['clearance']).all()

def invalid(m):
    args=[np.zeros((1,1,1,3)),np.zeros((1,1,1)),np.zeros((1,1,1),bool),np.zeros((1,1,1),bool),[0],[.1],1]
    for i,value in [(0,[[[[np.nan,0,0]]]]),(1,[[[1e5]]]),(4,[1]),(4,[False]),(5,[-.1]),(6,True),(6,10**1000),(6,np.int64(1))]:
        a=args.copy();a[i]=value;bad(lambda:m.terrain_clearance_report(*a))
TESTS=[('Supported and absent terrain slices','public',first),('Equality threshold and stance exclusion','public',stance),('Independent scalar grouping with realistic noncontiguous data','hidden',oracle),('Empty all-stance and negative-clearance evidence','hidden',boundaries),('Malformed geometry masked values and terrain IDs','hidden',invalid)]
