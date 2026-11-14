# Worked examples

### Example 1

B1,T2,H1,W2,C1: target valid firstframe[0,1],prediction[.2,.8],secondframe padded; valid[[True,False]] -> loss.04,per_horizon[.04,NaN],counts[1,0],has_dataTrue.

### Example 2

B2,T2,one-pixel target0; prediction[[0,1],[1,NaN]],valid[[True,True],[True,False]] -> loss2/3,per_horizon[.5,1],counts[2,1].
