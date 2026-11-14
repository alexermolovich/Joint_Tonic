"""Original deterministic inverse-grammar fixtures, CC0-1.0."""
import numpy as np
from numpy.testing import assert_array_equal


def complete_rows(m):
    bins,flags=m.parse_action_tokens(np.array([[0,41,99],[1,7,41]],dtype=np.int64),np.array([41,7,99],dtype=np.int64))
    assert isinstance(bins,np.ndarray) and isinstance(flags,np.ndarray)
    assert bins.dtype==flags.dtype==np.int64
    assert_array_equal(bins,[[0,2],[1,0]]);assert_array_equal(flags,[0,1])


def terminated_row(m):
    bins,flags=m.parse_action_tokens(np.array([[1,7]],dtype=np.int64),np.array([41,7,99],dtype=np.int64))
    assert_array_equal(bins,[[1]]);assert_array_equal(flags,[1])
    with np.testing.assert_raises(ValueError):m.parse_action_tokens(np.array([[0,41,1]],dtype=np.int64),np.array([41,7,99],dtype=np.int64))


def empty_rows(m):
    bins,flags=m.parse_action_tokens(np.empty((0,65),dtype=np.int64),np.array([2,1_000_000],dtype=np.int64))
    assert bins.shape==(0,64) and flags.shape==(0,) and bins.dtype==flags.dtype==np.int64


def noncontiguous_oracle(m):
    rng=np.random.default_rng(20261113);v=rng.choice(np.arange(2,1000001,dtype=np.int64),4096,replace=False)[::-1]
    expected=rng.integers(0,4096,size=(1024,64),dtype=np.int64);flags=rng.integers(0,2,1024,dtype=np.int64)
    data=np.empty((1024,130),dtype=np.int64);tokens=data[:,::2];tokens[:,0]=flags
    for row in range(1024):
        for column in range(64):tokens[row,column+1]=v[expected[row,column]]
    original=tokens.copy();v_before=v.copy();bins,actual_flags=m.parse_action_tokens(tokens,v)
    assert_array_equal(bins,expected);assert_array_equal(actual_flags,flags)
    assert bins.dtype==actual_flags.dtype==np.int64
    for out in (bins,actual_flags):
        assert not np.shares_memory(out,tokens) and not np.shares_memory(out,v)
    assert not np.shares_memory(bins,actual_flags)
    bins[:]=-1;actual_flags[:]=-1;assert_array_equal(tokens,original);assert_array_equal(v,v_before)


def invalid_fields(m):
    v=np.array([2,1_000_000],dtype=np.int64)
    for tokens in [np.array([[2,2]]),np.array([[-1,2]]),np.array([[0,0]]),np.array([[1,1]]),np.array([[0,99]]),np.array([[0,2],[1,999999]])]:
        with np.testing.assert_raises(ValueError):m.parse_action_tokens(tokens.astype(np.int64),v)
    bins,flags=m.parse_action_tokens(np.array([[0,1_000_000,2]],dtype=np.int64),v)
    assert_array_equal(bins,[[1,0]]);assert_array_equal(flags,[0])


def invalid_vocabulary(m):
    tokens=np.array([[0,2]],dtype=np.int64)
    for bad in [np.array([2,2]),np.array([1,2]),np.array([0,2]),np.array([-3,2]),np.array([2,1_000_001]),np.array([2]),np.arange(2,4099),np.array([[2,3]])]:
        with np.testing.assert_raises(ValueError):m.parse_action_tokens(tokens,bad.astype(np.int64))


def typed_shapes(m):
    args=[np.array([[0,7]],dtype=np.int64),np.array([7,8],dtype=np.int64)]
    for index in range(2):
        bad=args.copy();bad[index]=bad[index].tolist()
        with np.testing.assert_raises(TypeError):m.parse_action_tokens(*bad)
        for dtype in [np.int32,np.float64,np.bool_]:
            bad=args.copy();bad[index]=bad[index].astype(dtype)
            with np.testing.assert_raises(ValueError):m.parse_action_tokens(*bad)
    for value in [np.zeros((1025,2),dtype=np.int64),np.zeros((1,1),dtype=np.int64),np.zeros((1,66),dtype=np.int64),np.zeros(2,dtype=np.int64)]:
        with np.testing.assert_raises(ValueError):m.parse_action_tokens(value,args[1])


TESTS=[("Decode complete action rows","public",complete_rows),("Termination still requires action fields","public",terminated_row),("Empty row batch","public",empty_rows),
       ("Independent inverse oracle and nonaliasing at scale","hidden",noncontiguous_oracle),("Invalid fields reject whole batch","hidden",invalid_fields),("Vocabulary contract","hidden",invalid_vocabulary),("Typed shape contract","hidden",typed_shapes)]
