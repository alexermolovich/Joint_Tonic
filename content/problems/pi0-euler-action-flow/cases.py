"""Original deterministic flow-integration fixtures, CC0-1.0."""
import numpy as np
from numpy.testing import assert_allclose,assert_array_equal


def constant_field(m):
    calls=[]
    def field(state,time):
        assert type(time) is float;calls.append(time);return np.full_like(state,4.)
    final,trace=m.euler_action_flow(np.array([[[2.]]]),np.array([0.,.25,1.]),field)
    assert_array_equal(final,[[[6.]]]);assert_array_equal(trace[:,0,0,0],[2,3,6]);assert calls==[0.,.25]


def changing_state(m):
    received=[]
    def field(state,time):received.append(state);return state
    final,trace=m.euler_action_flow(np.array([[[1.]]]),np.array([0.,.5,1.]),field)
    assert_array_equal(final,[[[2.25]]]);assert_array_equal(trace[:,0,0,0],[1,1.5,2.25])
    assert_array_equal(received[0],[[[1.]]]);assert_array_equal(received[1],[[[1.5]]])


def state_and_time(m):
    final,trace=m.euler_action_flow(np.array([[[1.]]]),np.array([0.,.25,1.]),lambda x,t:x+2*t)
    assert_array_equal(trace[:,0,0,0],[1,1.25,2.5625]);assert_array_equal(final,[[[2.5625]]])


def storage_and_oracle(m):
    initial=np.arange(24.,dtype=np.float64).reshape(2,3,4)[:,:,::2]
    times=np.array([0.,9.,.1,9.,.4,9.,1.,9.])[::2];old=[x.copy() for x in (initial,times)]
    field_outputs=[]
    def field(x,t):
        value=(x*.2+t)[:,:,::-1][:,:,::-1];field_outputs.append((value,value.copy()));return value
    final,trace=m.euler_action_flow(initial,times,field)
    expected=[old[0].copy()]
    for a,b in zip(times[:-1],times[1:]):
        out=expected[-1].copy()
        for index in np.ndindex(out.shape):out[index]=expected[-1][index]+float(b-a)*(.2*expected[-1][index]+float(a))
        expected.append(out)
    assert final.dtype==trace.dtype==np.float64 and trace.shape==(4,2,3,2)
    assert_allclose(trace,np.stack(expected),rtol=1e-12,atol=1e-12);assert_array_equal(final,trace[-1])
    assert not np.shares_memory(final,trace)
    for out in (final,trace):
        for x in (initial,times):assert not np.shares_memory(out,x)
    final[:]=999;assert_allclose(trace,np.stack(expected),rtol=1e-12,atol=1e-12)
    for x,before in zip((initial,times),old):assert_array_equal(x,before)
    for value,before in field_outputs:assert_array_equal(value,before)


def scale_and_state_bounds(m):
    initial=np.zeros((8,32,16));times=np.linspace(0,1,129);calls=[]
    def field(x,t):calls.append(t);return np.full_like(x,3.)
    final,trace=m.euler_action_flow(initial,times,field)
    assert len(calls)==128 and trace.shape==(129,8,32,16)
    assert_allclose(final,3.,rtol=1e-12,atol=1e-12)
    final,trace=m.euler_action_flow(np.full((1,1,1),1e6),np.array([0.,.5,1.]),lambda x,t:np.full_like(x,1e6))
    assert_array_equal(final,[[[2e6]]]);assert_array_equal(trace[:,0,0,0],[1e6,1.5e6,2e6])


def input_contracts(m):
    initial=np.zeros((1,2,3));times=np.array([0.,1.]);field=lambda x,t:np.zeros_like(x)
    for a,b,c in [(initial.tolist(),times,field),(initial,times.tolist(),field),(initial,times,None)]:
        with np.testing.assert_raises(TypeError):m.euler_action_flow(a,b,c)
    for bad in [initial.astype(np.float32),initial[0],np.zeros((0,2,3)),np.zeros((17,2,3)),np.zeros((1,65,3)),np.zeros((1,2,33)),np.full_like(initial,np.nan),np.full_like(initial,1e6+1)]:
        with np.testing.assert_raises(ValueError):m.euler_action_flow(bad,times,field)
    for bad in [times.astype(np.float32),times.reshape(1,2),np.array([0.]),np.linspace(0,1,130),np.array([0.,np.nan,1.]),np.array([.01,1.]),np.array([0.,.99]),np.array([0.,.5,.5,1.]),np.array([0.,.75,.5,1.])]:
        with np.testing.assert_raises(ValueError):m.euler_action_flow(initial,bad,field)
    with np.testing.assert_raises(ValueError):m.euler_action_flow(np.zeros((16,64,32)),np.linspace(0,1,129),field)


def field_contracts(m):
    initial=np.zeros((1,2,3));times=np.array([0.,1.])
    for result in [None,initial.tolist(),initial.astype(np.float32),initial[0],np.zeros((1,2,1)),np.full_like(initial,np.inf),np.full_like(initial,np.nan),np.full_like(initial,1e6+1)]:
        with np.testing.assert_raises(ValueError):m.euler_action_flow(initial,times,lambda x,t:result)
    marker=RuntimeError("Original callback failure")
    def raises(x,t):raise marker
    try:m.euler_action_flow(initial,times,raises)
    except RuntimeError as error:assert error is marker
    else:raise AssertionError("Callback exception must propagate")


TESTS=[("Constant field on nonuniform times","public",constant_field),("Updated state and aliased callback result","public",changing_state),("Left-endpoint time conditioning","public",state_and_time),
       ("Independent scalar trace and storage","hidden",storage_and_oracle),("Step count and bounded accumulated state","hidden",scale_and_state_bounds),("Input type shape and grid contracts","hidden",input_contracts),("Callback returns and original exception","hidden",field_contracts)]
