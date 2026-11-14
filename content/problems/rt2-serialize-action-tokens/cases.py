"""Original deterministic action-token fixtures, CC0-1.0."""
import numpy as np
from numpy.testing import assert_array_equal


def example_mapping(m):
    out=m.serialize_action_tokens(np.array([[0,2],[1,0]],dtype=np.int64),np.array([41,7,99],dtype=np.int64),np.array([0,1],dtype=np.int64))
    assert isinstance(out,np.ndarray) and out.dtype==np.int64 and out.shape==(2,3)
    assert_array_equal(out,[[0,41,99],[1,7,41]])


def one_channel(m):
    out=m.serialize_action_tokens(np.array([[1]],dtype=np.int64),np.array([100,3],dtype=np.int64),np.array([0],dtype=np.int64))
    assert_array_equal(out,[[0,3]])


def empty_batch(m):
    out=m.serialize_action_tokens(np.empty((0,64),dtype=np.int64),np.array([2,1_000_000],dtype=np.int64),np.empty(0,dtype=np.int64))
    assert out.shape==(0,65) and out.dtype==np.int64


def storage_and_scale(m):
    rng=np.random.default_rng(20261113)
    vocabulary=rng.choice(np.arange(2,1000001,dtype=np.int64),4096,replace=False)[::-1]
    bins=rng.integers(0,4096,size=(64,1024),dtype=np.int64).T
    flags=np.arange(2048,dtype=np.int64)[::2]//2%2
    original=[x.copy() for x in (bins,vocabulary,flags)]
    out=m.serialize_action_tokens(bins,vocabulary,flags)
    expected=np.array([[int(flags[row])]+[int(vocabulary[int(q)]) for q in bins[row]] for row in range(1024)],dtype=np.int64)
    assert out.dtype==np.int64 and out.shape==(1024,65);assert_array_equal(out,expected)
    for x,before in zip((bins,vocabulary,flags),original):
        assert_array_equal(x,before);assert not np.shares_memory(out,x)
    out[:]=-9
    for x,before in zip((bins,vocabulary,flags),original):assert_array_equal(x,before)


def vocabulary_and_values(m):
    bins=np.array([[0,1]],dtype=np.int64);v=np.array([2,1_000_000],dtype=np.int64);flags=np.array([1],dtype=np.int64)
    assert_array_equal(m.serialize_action_tokens(bins,v,flags),[[1,2,1_000_000]])
    for bad in [np.array([2,2]),np.array([1,2]),np.array([0,2]),np.array([-3,2]),np.array([2,1_000_001])]:
        with np.testing.assert_raises(ValueError):m.serialize_action_tokens(bins,bad,flags)
    for bad in [np.array([[-1,0]]),np.array([[0,2]])]:
        with np.testing.assert_raises(ValueError):m.serialize_action_tokens(bad,v,flags)
    for bad in [np.array([-1]),np.array([2])]:
        with np.testing.assert_raises(ValueError):m.serialize_action_tokens(bins,v,bad)


def typed_shapes(m):
    args=[np.zeros((1,2),dtype=np.int64),np.array([7,8],dtype=np.int64),np.array([0],dtype=np.int64)]
    for index in range(3):
        bad=args.copy();bad[index]=bad[index].tolist()
        with np.testing.assert_raises(TypeError):m.serialize_action_tokens(*bad)
        for dtype in [np.int32,np.float64,np.bool_]:
            bad=args.copy();bad[index]=bad[index].astype(dtype)
            with np.testing.assert_raises(ValueError):m.serialize_action_tokens(*bad)
    for index,value in [(0,np.zeros((1025,2),dtype=np.int64)),(0,np.zeros((1,0),dtype=np.int64)),(0,np.zeros((1,65),dtype=np.int64)),(0,np.zeros(2,dtype=np.int64)),(1,np.array([7],dtype=np.int64)),(1,np.arange(2,4099,dtype=np.int64)),(1,np.array([[7,8]],dtype=np.int64)),(2,np.zeros((1,1),dtype=np.int64))]:
        bad=args.copy();bad[index]=value
        with np.testing.assert_raises(ValueError):m.serialize_action_tokens(*bad)


TESTS=[("Nonmonotone action vocabulary","public",example_mapping),("One action channel","public",one_channel),("Empty batch","public",empty_batch),
       ("Independent mapping oracle and storage at scale","hidden",storage_and_scale),("Reserved IDs and value boundaries","hidden",vocabulary_and_values),("Typed and bounded shape contract","hidden",typed_shapes)]
