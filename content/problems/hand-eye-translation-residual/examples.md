## Worked examples

1. Let both A translations be zero, R_A1=diag(1,-1,-1), R_A2=diag(-1,1,-1), and R_X=I. Use B with the same respective rotations and translations `[0,-4,-6]`, `[-2,0,-6]`. Return t=`[1,2,3]` and zero residuals.
2. Same rotations with every A/B translation zero returns t=`[0,0,0]` and zero residuals. Repeating only the first rotation instead must raise ValueError.
