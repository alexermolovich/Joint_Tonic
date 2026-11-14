# Worked examples

## Greedy matching can fail

cost=[[1,2],[2,100]], float64. Return [1,0], with total2+2=4. Choosing query0 for target0 greedily would force target1 to pay100, total101.

## More queries than targets

cost=[[4,1],[1,5],[3,3]], float64. Return [1,0], total1+1=2. Query2 is unused. For an all-zero2x2 matrix either [0,1] or [1,0] is accepted.
