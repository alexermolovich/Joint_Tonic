# Worked examples

## Unequal scaling

transforms=[[[2,0],[0,1]]], float64. A A.T-I=diag(3,0), so loss=9.

## Average over clouds only

transforms=[[[1,0],[0,1]],[[2,0],[0,1]]], float32. Per-cloud penalties0 and9 give loss4.5. Do not divide by the four matrix entries.
