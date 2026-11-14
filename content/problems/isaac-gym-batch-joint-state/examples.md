# Worked examples

### Example 1

flat_state=[[1,10],[2,20],[3,30],[4,40]], indices=[[2,0],[3,1]] -> [[[3,30],[1,10]],[[4,40],[2,20]]].

### Example 2

flat_state shape(0,2), indices shape(0,3) -> shape(0,3,2). Repeated selected index raises ValueError.
