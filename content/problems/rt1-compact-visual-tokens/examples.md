# Worked cases

### Case1: two attention maps and one padded location

```text
features = [[[1,0], [3,2], [9,9]]]
logits = [[[0,ln(3),99], [0,0,99]]]
valid = [[True,True,False]]

tokens  = [[[2.5,1.5], [2,1]]]
weights = [[[0.25,0.75,0], [0.5,0.5,0]]]
```

Construct `ln(3)` in the chosen float dtype. The first token is `0.25*[1,0]+0.75*[3,2]`; the large masked logit contributes nothing. The second averages the two valid locations.

### Case2: independent single-location images

```text
features = [[[2]], [[-4]]]
logits = [[[1000]], [[-1000]]]
valid = None

tokens = [[[2]], [[-4]]]
weights = [[[1]], [[1]]]
```

Each batch item normalizes its own spatial axis. The large difference between images’ logits is irrelevant.

## Additional public edge case

For features shape(1,2,1), logits shape(1,1,2), and valid=[[False,False]], raise ValueError. There is no valid probability distribution to return; do not substitute a uniform or zero-token fallback.

All values are original synthetic fixtures. These examples define visible behavior; they are not hidden test data.
