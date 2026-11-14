# Worked examples

## One frequency

positions=[[0,0.5,1]], levels=1. Output approximately [[0,1,0,1,0,-1]]. First three entries are sine, next three cosine.

## Two frequencies

positions=[[0.25,0,0]], levels=2. Let r=sqrt(2)/2. Output [[r,0,0,r,1,1,1,0,0,0,1,1]]. The second level uses 2*pi; tiny trigonometric rounding near zero is accepted.
