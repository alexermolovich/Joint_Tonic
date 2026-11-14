# Worked cases

### Case1: three chunks predicting tick2

```text
predictions = [[[0],[0],[2]], [[0],[4],[0]], [[8],[0],[0]]]
start_ticks = [0,1,2]   # int64
valid = [[True,True,True], [True,True,True], [True,True,True]]
target_tick = 2
decay = ln(2)

action = [24/7]         # approximately3.4285714286
weights = [4/7,2/7,1/7]
```

Selected entries are predictions[0,2]=2, predictions[1,1]=4, and predictions[2,0]=8. Raw weights are1,1/2,1/4. The oldest prediction receives the largest weight.

### Case2: a real zero prediction remains eligible

```text
predictions = [[[7],[7],[0]], [[10],[20],[30]]]
start_ticks = [5,7]   # int64
valid = [[True,True,True], [True,True,True]]
target_tick = 7
decay = 0

action = [5]
weights = [0.5,0.5]
```

The selected values are0 and10. Their mean is5; excluding a zero-valued prediction would incorrectly return10.

## Additional public edge case

In Case2, changing valid[0,2] toFalse yields action=[10] and weights=[0,1]. If both selected entries areFalse, raise ValueError. Masked chunks do not occupy ranks in the exponent.

All values are original synthetic fixtures. These examples define visible behavior; they are not hidden test data.
