# Worked cases

### Case1: a complete window and a padded tail

```text
actions = [[1],[2],[3]]
start_indices = [0,2]   # int64
horizon = 2

chunks = [[[1],[2]], [[3],[0]]]
valid = [[True,True], [True,False]]
```

The second window begins at the last real action. Its second slot has no target, so it is zero and invalid.

### Case2: preserve unsorted duplicate starts

```text
actions = [[2,-1],[4,3]]
start_indices = [1,0,1]   # int64
horizon = 3

chunks = [
  [[4,3],[0,0],[0,0]],
  [[2,-1],[4,3],[0,0]],
  [[4,3],[0,0],[0,0]]
]
valid = [[True,False,False], [True,True,False], [True,False,False]]
```

There is no deduplication or sorting. Every output row corresponds to the same-position entry of start_indices.

## Additional public edge case

With actions=np.array([[0,0]],dtype=np.float64), empty int64 start_indices, and horizon=3, return float64 shape(0,3,2) and bool shape(0,3). With start_indices=[0], the first zero action is valid and only later padding is invalid.

All values are original synthetic fixtures. These examples define visible behavior; they are not hidden test data.
