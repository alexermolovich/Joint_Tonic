# Worked examples

1. `points=[[1,2],[-1,3]], weights=I₂, bias=[0,-2]` gives local `[[1,0],[0,1]]` and global `[1,1]`.
2. A single point `[[2]]`, weight `[[-3]]`, bias `[1]` gives local `[[0]]` and global `[0]`: ReLU happens before pooling.
