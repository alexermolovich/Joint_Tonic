# Worked examples

### Example 1

one-pixel images[0,.2,.4],actions[[1],[2]],observed allTrue,episodes[0,0,0],starts[0],horizon3 -> current[0,.2,0],next[.2,.4,0],actions[1,2,0],valid[True,True,False] (shown without singleton axes).

### Example 2

Same data with episodes[0,1,1] and start0,horizon2 -> both transitions invalid; the second transition belongs to a different episode from the window start.
