# Batch Variable-Length Episodes with Masks

Implement batch_episodes(episodes: list[np.ndarray]) -> tuple[np.ndarray,np.ndarray,np.ndarray].

episodes is a Python list of B NumPy float64 arrays with1<=B<=128. Array b has shape(T_b,D),0<=T_b<=10000,1<=D<=128. Every episode has the same D. Values are finite with abs<=1e6 and may be noncontiguous. They are already aligned samples in the same channel order, units, frame and control convention; this function cannot establish compatibility from numbers alone.

Let L=max(T_b). Require B*L*D<=2,000,000, counting the padded output, not just observed values. Return (batch,valid,lengths):
- batch: new float64 array(B,L,D), containing each episode at batch[b,:T_b,:] and exact zero padding afterward.
- valid: new bool array(B,L), true exactly for timestep indices t<T_b.
- lengths: new int64 array(B,), containing each T_b.

All arrays have independent storage from every input and from each other; preserve inputs. Empty episodes are allowed and entirely masked. If all episodes are empty, shapes are(B,0,D),(B,0),(B,). An empty outer list is invalid because no feature width is available. No truncation, repeated-final-state padding, sorting, concatenation across episodes, timestamps or RNG. Every malformed type, shape, value, inconsistent width or exceeded bound raises ValueError.

## Worked examples

### Two episodes with different lengths

~~~python
batch_episodes([np.array([[1.,2.],[3.,4.]]),np.array([[5.,6.]])])
# batch = [[[1.,2.],[3.,4.]], [[5.,6.],[0.,0.]]]
# valid = [[True,True],[True,False]]
# lengths = [2,1] (int64)
~~~

The shorter episode does not borrow the first episode's second sample.

### An empty episode and a real zero sample

~~~python
batch_episodes([np.empty((0,1)),np.array([[0.]])])
# batch = [[[0.]],[[0.]]]
# valid = [[False],[True]]
# lengths = [0,1] (int64)
~~~

Equal numeric zeros have different validity. The mask, not the value, establishes whether a timestep exists.

## Source and scope

robomimic motivates careful offline data handling and comparing supervised objectives with closed-loop evaluation. The exact bounded interface and deterministic policy here are original teaching choices, not the complete robomimic data loader or evaluation system. [Primary source](https://arxiv.org/abs/2108.03298).

