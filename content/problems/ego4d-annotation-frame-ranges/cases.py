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

def example1(m):np.testing.assert_array_equal(m.annotation_frame_ranges(i([0,10,25,40]),i([[10,40],[11,24],[50,60]])),[[1,3],[2,2],[4,4]])
def example2(m):np.testing.assert_array_equal(m.annotation_frame_ranges(i([]),i([[0,1]])),[[0,0]])
def edges(m):
 hi=2**63-1;np.testing.assert_array_equal(m.annotation_frame_ranges(i([hi-3,hi-2,hi-1]),i([[hi-2,hi]])),[[1,3]])
 r=m.annotation_frame_ranges(i([1]),np.zeros((0,2),dtype=np.int64));assert r.shape==(0,2) and r.dtype==np.int64
def oracle_scale(m):
 times=np.arange(2000000,dtype=np.int64)[::2];left=np.arange(0,1000000,10,dtype=np.int64);intervals=np.stack([left,left+11],axis=1);before=[times.copy(),intervals.copy()];r=m.annotation_frame_ranges(times,intervals);np.testing.assert_array_equal(r[:,0],(left+1)//2);np.testing.assert_array_equal(r[:,1],(left+12)//2);unchanged(before,[times,intervals])
 rng=np.random.default_rng(937);times=np.sort(rng.choice(10000,200,replace=False)).astype(np.int64);intervals=np.array([[x,x+25] for x in range(0,10000,133)],dtype=np.int64);r=m.annotation_frame_ranges(times,intervals)
 for row,(a,z) in enumerate(intervals):assert tuple(r[row])==(sum(t<a for t in times),sum(t<z for t in times))
def invalid(m):
 for times,intervals in [(i([1,1]),i([[0,2]])),(i([2,1]),i([[0,2]])),(i([-1]),i([[0,2]])),(i([1]),i([[2,2]])),(i([1]),i([[-1,2]])),(f([1]),i([[0,2]])),(i([1]),i([[0,1,2]]))]:reject(lambda:m.annotation_frame_ranges(times,intervals))

TESTS=[('Worked example 1','public',example1),('Worked example 2','public',example2),('Boundary and dtype semantics','hidden',edges),('Independent oracle, scale and preservation','hidden',oracle_scale),('Invalid documented inputs','hidden',invalid)]
