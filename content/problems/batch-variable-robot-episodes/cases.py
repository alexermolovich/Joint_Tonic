from copy import deepcopy
from fractions import Fraction
import numpy as np

def invalid(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError("Expected ValueError")

def unequal(m):
    batch,valid,lengths=m.batch_episodes([np.array([[1.,2.],[3.,4.]]),np.array([[5.,6.]])])
    assert np.array_equal(batch,[[[1,2],[3,4]],[[5,6],[0,0]]])
    assert np.array_equal(valid,[[True,True],[True,False]]) and np.array_equal(lengths,[2,1])
    assert batch.dtype==np.float64 and valid.dtype==bool and lengths.dtype==np.int64

def zero_vs_empty(m):
    batch,valid,lengths=m.batch_episodes([np.empty((0,1)),np.array([[0.]])])
    assert np.array_equal(batch,np.zeros((2,1,1))) and np.array_equal(valid,[[False],[True]])
    assert np.array_equal(lengths,[0,1])

def all_empty(m):
    batch,valid,lengths=m.batch_episodes([np.empty((0,3)),np.empty((0,3))])
    assert batch.shape==(2,0,3) and valid.shape==(2,0) and np.array_equal(lengths,[0,0])

def malformed(m):
    for episodes in [None,(),[],[[]],[np.ones(2)],[np.ones((2,0))],[np.ones((1,129))],
                     [np.ones((1,2),dtype=np.float32)],[np.ones((1,1)),np.ones((1,2))],
                     [np.array([[np.nan]])],[np.array([[np.inf]])],[np.array([[1000001.]])],
                     [np.ones((10001,1))],[np.empty((0,1))]*129]:
        invalid(lambda:m.batch_episodes(episodes))

def independent_storage(m):
    a=np.arange(24.).reshape(4,6)[::2,::2];b=a[::-1];saved=[a.copy(),b.copy()]
    batch,valid,lengths=m.batch_episodes([a,b])
    assert np.array_equal(batch,np.stack(saved)) and valid.all() and np.array_equal(lengths,[2,2])
    for output in (batch,valid,lengths):
        assert not np.shares_memory(output,a) and not np.shares_memory(output,b)
    assert not np.shares_memory(batch,valid) and not np.shares_memory(batch,lengths)
    batch[0,0,0]=-1
    assert np.array_equal(a,saved[0]) and np.array_equal(b,saved[1])

def padded_budget(m):
    full=np.ones((10000,2))
    batch,valid,lengths=m.batch_episodes([full]+[np.empty((0,2))]*99)
    assert batch.shape==(100,10000,2) and int(valid.sum())==10000
    assert np.count_nonzero(batch[1:])==0
    invalid(lambda:m.batch_episodes([full]+[np.empty((0,2))]*100))

TESTS=[("Unequal episode lengths","public",unequal),("Real zeros and empty episodes","public",zero_vs_empty),("All-empty batch shapes","public",all_empty),
       ("Malformed episode contract","hidden",malformed),("Noncontiguous independent outputs","hidden",independent_storage),("Padded allocation budget","hidden",padded_budget)]

