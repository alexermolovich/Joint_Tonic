# Worked examples

### Different supported channels

~~~python
mask_action_dimensions(np.array([[1.,2.,3.],[4.,5.,6.]]),
                       np.array([[True,False,True],[False,True,False]]))
# [[1.,0.,3.],[0.,5.,0.]]
~~~

Only the supplied mask decides which values survive.

### Invalid placeholders are removed safely

~~~python
mask_action_dimensions(np.array([[np.nan,0.,np.inf]]),
                       np.array([[False,True,False]]))
# [[0.,0.,0.]]
~~~

The middle zero is a valid action. The other zeros replace unavailable values. Multiplication by a zero mask would leave NaN from the placeholders.

These examples use original synthetic fixtures. Hidden tests will exercise the same documented rules with different inputs.

