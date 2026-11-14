# Worked examples

## Flag and action rows share one logit width

Let vocabulary=[4,2], positions=[0,1], channels=2, all integer arrays int64. For float64 logits

~~~python
[[0, log(3), 50, 50, 50],
 [99, 99, 0, 99, log(3)]]
~~~

return tokens=[1,4] and probabilities=[[0.25,0.75,0,0,0],[0,0,0.25,0,0.75]]. Large forbidden logits never enter either normalizer.

## A tie follows token identity

With logits=[[0,0,0,0,0]], vocabulary=[4,2], positions=[2] and channels=2, return tokens=[2] and probabilities=[[0,0,0.5,0,0.5]]. Choosing the first vocabulary entry would incorrectly return 4.
