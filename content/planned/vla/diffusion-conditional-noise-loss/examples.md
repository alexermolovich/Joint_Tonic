# Worked cases

### Case1: padding does not contribute

```text
prediction = [[[1,3],[100,100]]]
target_noise = [[[0,1],[0,0]]]
valid = [[True,False]]

loss = scalar tensor2.5
```

The valid residual is[1,2], giving(1²+2²)/2=2.5. When prediction requires gradients, its gradient is[[[1,2],[0,0]]]. The padded100 values are finite but ignored by the objective.

### Case2: one global mean with unequal valid horizons

```text
prediction = [[[2],[0]], [[2],[4]]]
target_noise = [[[0],[0]], [[0],[0]]]
valid = [[True,False], [True,True]]

loss = scalar tensor8
```

There are three valid scalar errors:4,4,16. Their mean is8. Averaging per-item means would instead yield(4+10)/2=7, which is not this contract.

## Additional public edge case

An all-false valid mask raises ValueError, even when prediction and target_noise are all zeros. A single valid scalar with identical prediction/target returns a zero-dimensional zero tensor that remains connected to autograd when either input requires gradients.

All values are original synthetic fixtures. These examples define visible behavior; they are not hidden test data.
