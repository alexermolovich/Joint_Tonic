# Worked examples

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

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

