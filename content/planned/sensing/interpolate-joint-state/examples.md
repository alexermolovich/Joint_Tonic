# Worked inputs and expected outcomes

## Example 1: two joint channels

`times=[0,1]`, `q=[[0,2],[2,0]]`, `queries=[0.25,0.75]`, `max_gap=1`.

Expected aligned positions: `[[0.5,1.5],[1.5,0.5]]`; validity: `[True,True]`.

Both intervals meet the gap limit exactly. Angles use radians and are already unwrapped.

## Example 2: recorded values survive a dropout interval

`times=[0,2]`, `q=[[0],[2]]`, `queries=[0,1,2,3]`, `max_gap=0.5`.

Expected aligned positions: `[[0],[NaN],[2],[NaN]]`; validity: `[True,False,True,False]`.

Time 1 is bracketed but its two-second gap is too large. Time 3 would require extrapolation. Times 0 and 2 are exact recorded measurements, so they remain valid.
