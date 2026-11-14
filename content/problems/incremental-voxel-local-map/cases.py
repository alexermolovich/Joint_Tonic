import numpy as np
from numpy.testing import assert_allclose,assert_array_equal

def bad(fn):
    with np.testing.assert_raises(ValueError):fn()

def first(m):
    r=m.update_local_map(np.array([[.1,0,0],[.4,0,0]]),np.array([[.6,0,0]]),np.eye(4),np.zeros(3),np.full(3,2.),1);assert_allclose(r['points'],[[.4,0,0]]);assert_array_equal(r['source_indices'],[1]);assert_array_equal(r['removed_existing'],[True,False])
def negative(m):
    r=m.update_local_map(np.array([[-.1,0,0]]),np.zeros((1,3)),np.eye(4),np.zeros(3),np.full(3,2.),1);assert_array_equal(r['voxel_keys'],[[-1,0,0],[0,0,0]]);assert_array_equal(r['source_indices'],[0,1])
def oracle(m):
    rng=np.random.default_rng(856);old=rng.uniform(-10,10,(16384,6))[:,::2];scan=rng.uniform(-10,10,(16384,3));t=np.eye(4);t[:3,:3]=[[0,-1,0],[1,0,0],[0,0,1]];t[:3,3]=[2,-1,.5];center=np.array([1.,0,0]);extent=np.array([7.,6,5]);size=.5;before=old.copy();out=m.update_local_map(old,scan,t,center,extent,size);world=np.vstack([old,(t@np.c_[scan,np.ones(len(scan))].T).T[:,:3]]);ids=np.flatnonzero(np.all((world>=center-extent)&(world<=center+extent),axis=1));keys=np.floor(world[ids]/size).astype(np.int64);unique,group=np.unique(keys,axis=0,return_inverse=True);chosen=[]
    for g,key in enumerate(unique):
        candidates=ids[group==g];squared=np.sum((world[candidates]-(key+.5)*size)**2,axis=1);chosen.append(candidates[np.argmin(squared)])
    chosen=np.array(chosen);assert_array_equal(out['voxel_keys'],unique);assert_array_equal(out['source_indices'],chosen);assert_allclose(out['points'],world[chosen]);assert_array_equal(out['removed_existing'],~np.isin(np.arange(len(old)),chosen));assert_array_equal(old,before);assert not np.shares_memory(out['points'],old)
def empty_boundary(m):
    r=m.update_local_map(np.empty((0,3)),np.empty((0,3)),np.eye(4),np.zeros(3),np.ones(3),1);assert r['points'].shape==(0,3) and r['voxel_keys'].shape==(0,3);p=np.array([[1.,0,0],[1.0001,0,0],[-1,0,0]]);r=m.update_local_map(p,np.empty((0,3)),np.eye(4),np.zeros(3),np.ones(3),.1);assert_array_equal(r['source_indices'],[2,0]);assert_array_equal(r['removed_existing'],[False,True,False])
def invalid(m):
    args=[np.empty((0,3)),np.empty((0,3)),np.eye(4),np.zeros(3),np.ones(3),1]
    for i,v in [(5,10**1000),(5,0),(4,np.zeros(3)),(0,np.array([[np.nan,0,0]]))]:
        a=args.copy();a[i]=v;bad(lambda:m.update_local_map(*a))
TESTS=[('Center distance and stable identity tie','public',first),('Negative voxel floor','public',negative),('Independent grouped voxel oracle with rotated scan and full candidate scale','hidden',oracle),('Empty map and inclusive pruning boundaries','hidden',empty_boundary),('Invalid geometry and voxel scalars','hidden',invalid)]
