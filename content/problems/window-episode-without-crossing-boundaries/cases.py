import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def example(m):
    assert_array_equal(m.episode_windows([4,4,4,8,8],2,1),[[0,1],[1,2],[3,4]])
def stride(m):
    assert_array_equal(m.episode_windows([1,1,1,1,2],3,2),[[0,1,2]])
def empties(m):
    for ids in [[],[1,2,3]]:
        r=m.episode_windows(ids,2,1); assert r.shape==(0,2) and r.dtype==np.int64
    assert_array_equal(m.episode_windows([9,8],1,3),[[0],[1]])
def oracle(m):
    ids=np.repeat([5,3,99],[17,8,14]); old=ids.copy(); expected=[]; start=0
    for length in [17,8,14]:
        expected.extend([list(range(s,s+4)) for s in range(start,start+length-3,3)]); start+=length
    assert_array_equal(m.episode_windows(ids,4,3),expected); assert_array_equal(ids,old)
def invalid(m):
    for args in [([1,2,1],2,1),([-1],1,1),([.5],1,1),([True],1,1),([[1]],1,1),([1],0,1),([1],2,True),([1],2.,1),([1],1,10001)]:
        with np.testing.assert_raises(ValueError): m.episode_windows(*args)
TESTS=[('Episode boundaries','public',example),('Stride and incomplete tail','public',stride),('Empty windows','hidden',empties),('Independent run enumeration','hidden',oracle),('Invalid sequence contract','hidden',invalid)]
