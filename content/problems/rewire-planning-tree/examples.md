# Worked examples

1. Parents `[-1,0,1,0]`, edge costs `[0.,5.,2.,1.]`, vertex `1`, new parent `3`, connection cost `1`, feasible True yield parents `[-1,3,1,0]`, edge costs `[0.,1.,2.,1.]`, root costs `[0.,2.,4.,1.]`, changed True.
2. With the same original tree, connecting vertex `1` beneath vertex `2` would form a cycle. Return unchanged parents and edges, root costs `[0.,5.,7.,1.]`, changed False.
