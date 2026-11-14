import numpy as np
from numpy.testing import assert_array_equal,assert_allclose
def small(m):
    r=m.profile_vit(np.array([[4,4]],dtype=np.int64),2,2,4,np.array([[1.,2,3,4]]));assert_array_equal(r['tokens'],[5]);assert_array_equal(r['attention_bytes'],[200]);assert_allclose(r['p95_latency_ms'],[4])
def larger(m):
    r=m.profile_vit(np.array([[8,8]],dtype=np.int64),2,2,4,np.ones((1,1)));assert_array_equal(r['tokens'],[17]);assert_array_equal(r['attention_bytes'],[2312])
def percentile(m):
    r=m.profile_vit(np.array([[4,8],[2,2]],dtype=np.int64),2,3,2,np.stack([np.arange(20.,0,-1),np.arange(1.,21)]));assert_array_equal(r['tokens'],[9,2]);assert_array_equal(r['attention_bytes'],[486,24]);assert_allclose(r['p95_latency_ms'],[19,19])
def empty(m):
    r=m.profile_vit(np.empty((0,2),dtype=np.int64),1,1,2,np.empty((0,3)));assert all(x.shape==(0,) for x in r.values())
def invalid(m):
    for r,p,h,b,l in [(np.array([[3,4]],dtype=np.int64),2,2,4,np.ones((1,1))),(np.array([[4,4]],dtype=np.int64),True,2,4,np.ones((1,1))),(np.array([[4,4]],dtype=np.int64),2,2,3,np.ones((1,1))),(np.array([[4,4]],dtype=np.int64),2,2,4,np.zeros((1,1)))]:
        with np.testing.assert_raises(ValueError):m.profile_vit(r,p,h,b,l)
TESTS=[('Small grid','public',small),('Resolution scaling','public',larger),('Nearest-rank convention and nonsquare grids','hidden',percentile),('Empty resolution list','hidden',empty),('Validation','hidden',invalid)]

def scale_storage(m):
    resolutions=np.tile([32,0,64,0],(128,1)).astype(np.int64)[:,::2];latencies=np.tile(np.arange(1.,8193.),(128,1))[:,::2];saved=latencies.copy();r=m.profile_vit(resolutions,8,8,4,latencies)
    assert_array_equal(r['tokens'],np.full(128,33));assert_array_equal(r['attention_bytes'],np.full(128,8*33*33*4));rank=(95*4096+99)//100-1;assert_allclose(r['p95_latency_ms'],latencies[:,rank]);assert_allclose(latencies,saved)
    for out in r.values():assert not np.shares_memory(out,latencies)

TESTS.append(('Scale noncontiguous and preservation','hidden',scale_storage))
