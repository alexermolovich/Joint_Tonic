# Worked cases

### Case1: fractional time across a two-step action chunk

```text
actions = [[[2,-2],[4,6]]]
noise = [[[0,2],[2,2]]]
tau = [0.25]
valid = [[True,True]]

interpolant = [[[0.5,1],[2.5,3]]]
target_velocity = [[[2,-4],[2,4]]]
```

For the last scalar,0.75*2+0.25*6=3 and its velocity target is6-2=4. The same flow time applies to every action coordinate in this batch item.

### Case2: different endpoints for different batch items

```text
actions = [[[2]], [[-1]]]
noise = [[[6]], [[3]]]
tau = [0,1]
valid = [[True],[True]]

interpolant = [[[6]], [[-1]]]
target_velocity = [[[-4]], [[-4]]]
```

The first item is exactly noise at tau0; the second is exactly clean action at tau1. The velocity target does not vanish at either endpoint.

## Additional public edge case

In Case1, valid=[[True,False]] changes both second horizon vectors to[0,0]. With valid=[[False,False]], both outputs are all zeros and the call succeeds. An all-padding training loss may reject this later; construction and reduction have different contracts.

All values are original synthetic fixtures. These examples define visible behavior; they are not hidden test data.
