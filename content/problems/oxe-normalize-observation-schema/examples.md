## Example 1

raw={"p_cm":[[100],[200]]}, mapping={"position":"p_cm"}, scales={"position":0.01}, timestamps=[0,1] returns features={"position":[[1],[2]]} and timestamps=[0,1].

## Example 2

raw={"q":[[180]]}, mapping={"joint":"q","copy":"q"}, scales={"joint":pi/180,"copy":1}, timestamps=[2] returns joint=[[pi]] and copy=[[180]], with independent storage.
