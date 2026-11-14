# Worked examples

## A 2 by 2 image

Input: depth=[[1,2],[0,4]], K=[[2,0,0],[0,2,0],[0,0,1]].

Return points=[[0,0,1],[1,0,2],[NaN,NaN,NaN],[2,2,4]] and valid=[True,True,False,True]. The final pixel has u=v=1 and z=4 m.

## Offset principal point

Input: depth=[[2,NaN]], K=[[4,0,1],[0,2,0],[0,0,1]].

Return points=[[-0.5,0,2],[NaN,NaN,NaN]] and valid=[True,False]. Column zero is one pixel left of the principal point.
